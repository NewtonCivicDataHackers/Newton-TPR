#!/usr/bin/env python3

# /// script
# requires-python = ">=3.8"
# dependencies = [
#   "curl_cffi>=0.7.0",
#   "beautifulsoup4>=4.9.0",
# ]
# ///

import os
import sys
import argparse
from curl_cffi import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# newtonma.gov sits behind Akamai bot protection, which fingerprints the TLS
# handshake itself — spoofed browser headers on a plain requests/urllib client
# get a 403. curl_cffi impersonates a real Chrome TLS fingerprint (and sets
# matching headers), which passes the check.
IMPERSONATE = 'chrome'

def make_session(cookies=None, referer=None):
    """
    Create a curl_cffi session impersonating Chrome.

    Args:
        cookies: Optional list of cookies in format ["name=value", ...]
        referer: Optional referer URL to use in request headers

    Returns:
        requests.Session: Configured session
    """
    session = requests.Session(impersonate=IMPERSONATE)

    if referer:
        session.headers['Referer'] = referer
        print(f"Using referer: {referer}")

    if cookies:
        for cookie_str in cookies:
            try:
                name, value = cookie_str.split('=', 1)
                session.cookies.set(name, value)
                print(f"Added cookie: {name}")
            except ValueError:
                print(f"Warning: Invalid cookie format: {cookie_str}. Expected 'name=value'")

    return session

def get_tpr_document(url, output_file, cookies=None, referer=None):
    """
    Retrieve the TPR document from the given URL.

    Args:
        url: The URL to the Newton MA Transportation Division page
        output_file: Path to save the downloaded TPR document
        cookies: Optional list of cookies in format ["name=value", ...]
        referer: Optional referer URL to use in request headers

    Returns:
        bool: True if successful, False otherwise
    """
    print(f"Fetching page: {url}")

    try:
        # Step 1: Get the transportation division page
        with make_session(cookies, referer) as session:
            response = session.get(url, timeout=30)
            response.raise_for_status()

            # Step 2: Parse the HTML and find the TPR link
            soup = BeautifulSoup(response.text, 'html.parser')

            # Look for links containing the TPR text
            tpr_link = None
            for link in soup.find_all('a'):
                link_text = link.get_text(strip=True)
                if "Traffic and Parking Regulations (TPR)" in link_text:
                    tpr_link = link.get('href')
                    break

            if not tpr_link:
                print("Error: Could not find the TPR document link on the page.")
                return False

            # Make sure we have an absolute URL
            if not tpr_link.startswith(('http://', 'https://')):
                tpr_link = urljoin(url, tpr_link)

            # Print this on a separate line so it can be easily extracted by scripts
            print(f"Found TPR document link: {tpr_link}")

            # Step 3: Download the TPR document
            pdf_response = session.get(tpr_link, timeout=60)
            pdf_response.raise_for_status()

            # Check if the response is a PDF
            content_type = pdf_response.headers.get('Content-Type', '')
            if 'application/pdf' not in content_type and not tpr_link.lower().endswith('.pdf'):
                print(f"Warning: The downloaded file may not be a PDF (Content-Type: {content_type})")

            # Step 4: Save the PDF to the output file
            with open(output_file, 'wb') as f:
                f.write(pdf_response.content)

            print(f"Successfully downloaded TPR document to: {output_file}")
            return True

    except Exception as e:
        print(f"Error during request: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Download the latest Newton Traffic and Parking Regulations document.')
    parser.add_argument('output_file', help='Path to save the downloaded TPR document')
    parser.add_argument('--url', default='https://www.newtonma.gov/government/public-works/transportation-division',
                        help='URL to the Newton Transportation Division page (default: %(default)s)')
    parser.add_argument('--direct-url',
                        help='Direct URL to the TPR PDF if known (bypasses searching the transportation page)')
    parser.add_argument('--cookie', action='append', default=[],
                        help='Cookie in format name=value. Can be specified multiple times for multiple cookies')
    parser.add_argument('--referer',
                        help='Referer URL to use in request headers')

    args = parser.parse_args()

    # Create the directory if it doesn't exist
    output_dir = os.path.dirname(args.output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # If direct URL is provided, download it directly
    if args.direct_url:
        print(f"Using direct PDF URL: {args.direct_url}")
        try:
            with make_session(args.cookie, args.referer) as session:
                response = session.get(args.direct_url, timeout=60)
                response.raise_for_status()

                with open(args.output_file, 'wb') as f:
                    f.write(response.content)

            print(f"Successfully downloaded TPR document to: {args.output_file}")
            return 0
        except Exception as e:
            print(f"Error downloading from direct URL: {e}")
            return 1

    # Otherwise use the normal process with requests
    success = get_tpr_document(args.url, args.output_file, args.cookie, args.referer)

    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
