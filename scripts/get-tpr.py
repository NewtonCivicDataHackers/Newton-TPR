#!/usr/bin/env python3

# /// script
# requires-python = ">=3.8"
# dependencies = [
#   "requests>=2.25.0",
#   "beautifulsoup4>=4.9.0",
# ]
# ///

import os
import sys
import argparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_default_headers(referer=None):
    """
    Returns a dictionary of default headers to mimic a Chrome browser on macOS.
    
    Args:
        referer: Optional referer URL to use in headers
        
    Returns:
        dict: Headers dictionary
    """
    headers = {
        'authority': 'www.newtonma.gov',
        'method': 'GET',
        'scheme': 'https',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-encoding': 'gzip, deflate, br, zstd',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    }
    
    # Add referer if provided
    if referer:
        headers['Referer'] = referer
        
    return headers

def get_tpr_document(url, output_file, cookies=None, referer=None):
    """
    Retrieve the TPR document from the given URL using requests.
    
    Args:
        url: The URL to the Newton MA Transportation Division page
        output_file: Path to save the downloaded TPR document
        cookies: Optional list of cookies in format ["name=value", ...]
        referer: Optional referer URL to use in request headers
    
    Returns:
        bool: True if successful, False otherwise
    """
    # Get headers with consolidated function
    headers = get_default_headers(referer)
    
    if referer:
        print(f"Using referer: {referer}")
    
    print(f"Fetching page with requests: {url}")
    
    try:
        # Step 1: Get the transportation division page
        with requests.Session() as session:
            # Add cookies if provided
            if cookies:
                for cookie_str in cookies:
                    try:
                        name, value = cookie_str.split('=', 1)
                        session.cookies.set(name, value)
                        print(f"Added cookie: {name}")
                    except ValueError:
                        print(f"Warning: Invalid cookie format: {cookie_str}. Expected 'name=value'")
            response = session.get(url, headers=headers, timeout=30)
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
            
            print(f"Found TPR document link: {tpr_link}")
            
            # Step 3: Download the TPR document
            pdf_response = session.get(tpr_link, headers=headers, timeout=60)
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
        
    except requests.exceptions.RequestException as e:
        print(f"Error during request: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
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
            # Get headers from consolidated function
            headers = get_default_headers(args.referer)
            
            if args.referer:
                print(f"Using referer: {args.referer}")
            
            # Create a session to handle cookies
            session = requests.Session()
            
            # Add cookies if provided
            if args.cookie:
                for cookie_str in args.cookie:
                    try:
                        name, value = cookie_str.split('=', 1)
                        session.cookies.set(name, value)
                        print(f"Added cookie: {name}")
                    except ValueError:
                        print(f"Warning: Invalid cookie format: {cookie_str}. Expected 'name=value'")
            
            response = session.get(args.direct_url, headers=headers, timeout=60)
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