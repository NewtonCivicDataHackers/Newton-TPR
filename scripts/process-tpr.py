#!/usr/bin/env python3

# /// script
# requires-python = ">=3.8"
# dependencies = [
#   "pdfminer.six>=20221105",
# ]
# ///

import os
import re
import sys
import json
import shutil
import argparse
import datetime
from io import StringIO
from pathlib import Path

# Import pdfminer components
from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams

def convert_pdf_to_text(pdf_path, output_path=None):
    """Convert PDF to text using pdfminer."""
    print(f"Converting PDF: {pdf_path}")
    
    output = StringIO()
    with open(pdf_path, 'rb') as pdf_file:
        extract_text_to_fp(
            pdf_file, 
            output,
            laparams=LAParams(
                line_margin=0.3,
                char_margin=2.0,
                word_margin=0.1
            ),
            output_type='text',
            codec='utf-8'
        )
    
    text = output.getvalue()
    
    # Save the text to file if output path is specified
    if output_path:
        print(f"Saving text to: {output_path}")
        with open(output_path, 'w', encoding='utf-8') as text_file:
            text_file.write(text)
    
    return text

def extract_revision_date(text):
    """Extract the revision date from the TPR document."""
    # Pattern to match "Updated through Month Day, Year" with variations
    patterns = [
        r'Updated\s+through\s+(\w+)\s+(\d{1,2}),\s+(\d{4})',
        r'Updated\s+to\s+(\w+)\s+(\d{1,2}),\s+(\d{4})',
        r'Revised\s+through\s+(\w+)\s+(\d{1,2}),\s+(\d{4})',
        r'As\s+of\s+(\w+)\s+(\d{1,2}),\s+(\d{4})',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            month_name, day, year = match.groups()
            month_map = {
                'January': 1, 'February': 2, 'March': 3, 'April': 4,
                'May': 5, 'June': 6, 'July': 7, 'August': 8,
                'September': 9, 'October': 10, 'November': 11, 'December': 12
            }
            
            month = month_map.get(month_name, 1)  # Default to January if month not found
            day = int(day)
            year = int(year)
            
            # Format date as YYYY-MM-DD
            date_str = f"{year:04d}-{month:02d}-{day:02d}"
            return date_str
    
    # If no date found, use today's date
    today = datetime.date.today()
    return today.strftime("%Y-%m-%d")

def process_file(text):
    """Process the text to identify page breaks and prepare for section extraction."""
    print("Processing file to identify page breaks...")
    
    # Find all form feed positions
    form_feed_positions = []
    position = 0
    pages = []
    
    # Split by form feed characters to get pages
    page_texts = text.split('\f')
    
    for page_num, page_text in enumerate(page_texts, 1):
        if page_text.strip():  # Skip empty pages
            pages.append({
                'page_number': page_num,
                'content': page_text.splitlines()
            })
    
    # Process each page to add markers to original text for later processing
    processed_text = []
    
    for page in pages:
        page_num = page['page_number']
        processed_text.append(f'[PAGE_START:{page_num}]')
        processed_text.extend(page['content'])
        processed_text.append(f'[PAGE_END:{page_num}]')
    
    return pages, processed_text

def find_section_boundaries(processed_text):
    """Find the start and end lines for each section."""
    section_boundaries = {}
    current_section = None
    
    for i, line in enumerate(processed_text):
        # Check for section headers
        match = re.match(r'^Sec\.\s*TPR-(\d+)\.', line)
        if match:
            # If we were processing a section, mark its end
            if current_section is not None:
                section_boundaries[current_section]['end_line'] = i - 1
            
            # Start a new section
            current_section = match.group(1)
            section_boundaries[current_section] = {
                'start_line': i,
                'end_line': None  # Will be set later
            }
    
    # Set the end of the last section
    if current_section is not None and section_boundaries[current_section]['end_line'] is None:
        section_boundaries[current_section]['end_line'] = len(processed_text) - 1
    
    return section_boundaries

def find_section_page_ranges(pages, section_boundaries, processed_text):
    """Determine the page range for each section."""
    section_page_ranges = {}
    
    # Initialize page markers in the processed text
    page_markers = {}
    line_count = 0
    
    for page in pages:
        page_num = page['page_number']
        start_line = line_count
        line_count += 1  # For the [PAGE_START] marker
        line_count += len(page['content'])
        end_line = line_count - 1
        line_count += 1  # For the [PAGE_END] marker
        
        page_markers[page_num] = {
            'start_line': start_line,
            'end_line': end_line
        }
    
    # Map each section to its page range
    for section_num, boundaries in section_boundaries.items():
        section_start_line = boundaries['start_line']
        section_end_line = boundaries['end_line']
        
        start_page = None
        end_page = None
        
        # Find which page contains the section start
        for page_num, marker in page_markers.items():
            if marker['start_line'] <= section_start_line <= marker['end_line']:
                start_page = page_num
                break
        
        # Find which page contains the section end
        for page_num, marker in page_markers.items():
            if marker['start_line'] <= section_end_line <= marker['end_line']:
                end_page = page_num
                break
        
        section_page_ranges[section_num] = {
            'start_page': start_page,
            'end_page': end_page
        }
    
    return section_page_ranges

def extract_section_content(processed_text, section_boundaries):
    """Extract the content for each section."""
    section_content = {}
    
    for section_num, boundaries in section_boundaries.items():
        start_line = boundaries['start_line']
        end_line = boundaries['end_line']
        
        # Extract lines for this section, excluding page markers
        section_lines = []
        for i in range(start_line, end_line + 1):
            line = processed_text[i]
            if not line.startswith('[PAGE_'):
                section_lines.append(line)
        
        section_content[section_num] = section_lines
    
    return section_content

def clean_line(line):
    """Clean up a line of text, removing section markers and headers."""
    # Skip section markers at the beginning of lines
    if re.match(r'^\s*§\s*TPR-\d+', line):
        return None
    
    # Skip "NEWTON TRAFFIC AND PARKING REGULATIONS" headers
    if re.match(r'^\s*NEWTON TRAFFIC AND PARKING REGULATIONS\s*$', line):
        return None
    
    # Remove section markers within lines
    line = re.sub(r'§\s*TPR-\d+', '', line)
    
    # Remove section references in headers (including range references)
    line = re.sub(r'§§?\s*TPR-\d+(?:[—-]TPR-\d+)?', '', line)
    
    return line

def clean_section_content(section_lines):
    """Clean section content by removing headers and extra whitespace."""
    cleaned_lines = []
    blank_count = 0
    
    for line in section_lines:
        cleaned = clean_line(line)
        if cleaned is None:
            continue
            
        # Handle blank lines (condense multiple blank lines to just one)
        if cleaned.strip() == '':
            blank_count += 1
            if blank_count <= 1:  # Keep only the first blank line
                cleaned_lines.append(cleaned)
        else:
            blank_count = 0
            cleaned_lines.append(cleaned)
    
    return cleaned_lines

def extract_preamble(processed_text, first_section_start_line):
    """Extract the preamble content (before first section)."""
    preamble_lines = []
    found_tpr_header = False
    
    for i in range(first_section_start_line):
        line = processed_text[i]
        
        # Skip page markers
        if line.startswith('[PAGE_'):
            continue
            
        if 'TRAFFIC AND PARKING REGULATIONS' in line:
            found_tpr_header = True
        
        if found_tpr_header:
            # Stop at the first article header
            if 'ARTICLE I.' in line:
                break
                
            preamble_lines.append(line)
    
    return clean_section_content(preamble_lines)

def extract_section_title(section_content):
    """Extract the title from a section's content."""
    if not section_content:
        return "Reserved"
        
    first_line = section_content[0].strip()
    title_match = re.match(r'^Sec\.\s*TPR-\d+\.\s*(.+?)\.?\s*$', first_line)
    
    if title_match:
        return title_match.group(1).strip()
    else:
        return first_line.strip()

def get_file_size(file_path):
    """Get the size of a file in bytes."""
    return os.path.getsize(file_path)


def create_readme(index_data, sections_dir):
    """Create a README.md file with information about the document and a table of contents."""
    # Get the revision date from the index
    revision_date = index_data.get("revision_date", "Unknown")
    last_updated = index_data.get("last_updated", datetime.date.today().strftime("%Y-%m-%d"))
    source_file = index_data.get("source", "tpr.pdf")
    source_url = index_data.get("source_url")
    pdf_url = index_data.get("pdf_url")
    
    # Start building the README content
    readme_content = f"# Newton Traffic and Parking Regulations\n\n"
    readme_content += f"## Document Information\n\n"
    readme_content += f"- **Revision Date**: {revision_date}\n"
    readme_content += f"- **Last Processed**: {last_updated}\n"
    readme_content += f"- **Local Document**: [{source_file}]({source_file})\n"
    
    # Add source URLs if available
    if source_url:
        readme_content += f"- **Source Webpage**: [{source_url}]({source_url})\n"
    if pdf_url:
        readme_content += f"- **Original PDF**: [{pdf_url}]({pdf_url})\n"
    
    # Add extracted data reference if directory exists
    extracted_data_dir = os.path.join(os.path.dirname(sections_dir), "extracted_data")
    if os.path.exists(extracted_data_dir) and os.path.isdir(extracted_data_dir):
        readme_content += f"- **Extracted Data**: [extracted_data/](extracted_data/)\n"
    
    readme_content += "\n## Table of Contents\n\n"
    
    # Create a table header for the sections
    readme_content += "| Section | Title | Text | PDF Page | Size |\n"
    readme_content += "|---------|-------|------|----------|------|\n"
    
    # Add the preamble if it exists
    preamble_path = os.path.join(sections_dir, "00-preamble.txt")
    if os.path.exists(preamble_path):
        preamble_size = get_file_size(preamble_path)
        readme_content += f"| Preamble | TRAFFIC AND PARKING REGULATIONS | [00-preamble.txt](sections/00-preamble.txt) | - | {preamble_size} bytes |\n"
    
    # Add each section to the table
    for section in index_data["sections"]:
        section_num = section["section"]
        section_title = section.get("title", "Unknown")
        txt_filename = section["txt_filename"]
        page_start = section.get("page_start", "-")
        page_end = section.get("page_end", "-")
        
        # Calculate the section file size
        section_path = os.path.join(sections_dir, f"{section_num}.txt")
        if os.path.exists(section_path):
            section_size = get_file_size(section_path)
        else:
            section_size = 0
        
        # Create a link to the PDF page if page_start is available
        pdf_link = f"[{page_start}]({source_file}#page={page_start})" if page_start not in [None, "-"] else "-"
        
        # Add the row to the table
        readme_content += f"| {section_num} | {section_title} | [{section_num}.txt](sections/{section_num}.txt) | {pdf_link} | {section_size} bytes |\n"
    
    # Add Data Formats section if the extracted_data directory exists
    extracted_data_dir = os.path.join(os.path.dirname(sections_dir), "extracted_data")
    if os.path.exists(extracted_data_dir) and os.path.isdir(extracted_data_dir):
        readme_content += "\n## Data Formats\n\n"
        readme_content += "The Traffic and Parking Regulations have been processed into machine-readable CSV files in the [extracted_data/](extracted_data/) directory:\n\n"
        readme_content += "- Speed limits by street segment\n"
        readme_content += "- Traffic controls (signals, stop signs, yield signs)\n"
        readme_content += "- Turning restrictions (left turns, right turns, U-turns, no turn on red)\n"
        readme_content += "- Parking regulations (loading zones, fire lanes, accessible spaces)\n"
        readme_content += "- School zones and safety zones\n"
        readme_content += "- Commercial vehicle restrictions\n"
        readme_content += "- One-way streets\n"
    
    # Add additional information
    readme_content += "\n## Notes\n\n"
    readme_content += f"- This document contains the Traffic and Parking Regulations for the City of Newton, updated through {revision_date}.\n"
    readme_content += f"- The data in this repository was last processed on {last_updated}.\n"
    readme_content += "- Section files are provided in plain text format in the [sections](sections/) directory.\n"
    readme_content += "- For direct access to specific content, you can either:\n"
    readme_content += "  - Read the text files in the sections directory\n"
    readme_content += "  - View the local PDF by clicking on the page links in the table above\n"
    
    if pdf_url:
        readme_content += f"  - Access the [original PDF]({pdf_url}) on Newton's website\n"
    
    if source_url:
        readme_content += f"- The latest version of this document can be found on [Newton's Transportation Division website]({source_url}).\n"
        
    readme_content += "- Previous versions of this document can be found in the Git history.\n"
    
    return readme_content

def main():
    parser = argparse.ArgumentParser(description='Process a TPR document (PDF or text) and split it into sections.')
    parser.add_argument('input_file', help='Input PDF file to process')
    parser.add_argument('output_dir', help='Base directory to save processed files')
    parser.add_argument('--save-text', dest='save_text', action='store_true',
                        help='Save the intermediate text file after PDF conversion')
    parser.add_argument('--overwrite', dest='overwrite', action='store_true',
                        help='Force processing even if the document revision date has not changed')
    parser.add_argument('--extract-date-only', dest='extract_date_only', action='store_true',
                        help='Only extract and output the revision date in YYYY-MM-DD format')
    parser.add_argument('--source-url', dest='source_url',
                        help='URL of the source webpage where the PDF was found')
    parser.add_argument('--pdf-url', dest='pdf_url',
                        help='Direct URL to the source PDF document')
    args = parser.parse_args()
    
    # Check if input file exists
    if not os.path.isfile(args.input_file):
        print(f"Error: Input file '{args.input_file}' does not exist.")
        sys.exit(1)
    
    # Convert PDF to text
    text = convert_pdf_to_text(args.input_file)
    
    # Extract the revision date
    revision_date = extract_revision_date(text)
    print(f"Detected revision date: {revision_date}")
    
    # If only extracting date, print it and exit
    if args.extract_date_only:
        print(revision_date)
        return 0
    
    # Use the output directory directly instead of creating a date subdirectory
    output_dir = args.output_dir
    sections_dir = os.path.join(output_dir, "sections")
    
    # Check if the document has changed by comparing revision dates
    current_revision = None
    should_process = True
    index_path = os.path.join(output_dir, 'index.json')
    
    if os.path.exists(index_path):
        try:
            with open(index_path, 'r') as f:
                current_index = json.load(f)
                current_revision = current_index.get('revision_date')
                
                if current_revision == revision_date and not args.overwrite:
                    print(f"The document revision date ({revision_date}) matches the current version.")
                    print("No changes detected. Use --overwrite to force processing.")
                    return 0
                    
                print(f"Current revision: {current_revision}, New revision: {revision_date}")
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not read existing index.json: {e}")
    
    # Create directories
    os.makedirs(sections_dir, exist_ok=True)
    
    # Copy PDF file to the output directory
    pdf_dest = os.path.join(output_dir, "tpr.pdf")
    shutil.copy2(args.input_file, pdf_dest)
    print(f"Copied PDF to: {pdf_dest}")
    
    # Save the text file if requested
    if args.save_text:
        text_file = os.path.join(output_dir, "tpr.txt")
        with open(text_file, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"Saved text to: {text_file}")
    
    # Process the file to detect form feeds and page boundaries
    pages, processed_text = process_file(text)
    print(f"Found {len(pages)} pages in the document")
    
    # Find section boundaries in the processed text
    section_boundaries = find_section_boundaries(processed_text)
    print(f"Found {len(section_boundaries)} sections in the document")
    
    # Determine page ranges for each section
    section_page_ranges = find_section_page_ranges(pages, section_boundaries, processed_text)
    
    # Extract the preamble (before the first section)
    first_section_key = min(section_boundaries.keys(), key=int)
    first_section_start_line = section_boundaries[first_section_key]['start_line']
    preamble_lines = extract_preamble(processed_text, first_section_start_line)
    
    # Write the preamble file
    preamble_file = os.path.join(sections_dir, '00-preamble.txt')
    with open(preamble_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(preamble_lines))
    print(f"Created preamble file: {preamble_file}")
    
    # Extract and clean content for each section
    section_content = extract_section_content(processed_text, section_boundaries)
    
    # Create index data
    index = {
        "source": "tpr.pdf",
        "revision_date": revision_date,
        "last_updated": datetime.date.today().strftime("%Y-%m-%d"),
        "sections": []
    }
    
    # Add source URLs if provided
    if args.source_url:
        index["source_url"] = args.source_url
    if args.pdf_url:
        index["pdf_url"] = args.pdf_url
    
    # Process each section
    for section_num in sorted(section_content.keys(), key=int):
        section_lines = section_content[section_num]
        page_range = section_page_ranges.get(section_num, {'start_page': None, 'end_page': None})
        
        # Clean the section content
        clean_content = clean_section_content(section_lines)
        
        # Extract the section title
        section_title = extract_section_title(section_lines)
        
        # Create filename just with the section number
        file_name = f"{section_num}.txt"
        section_file = os.path.join(sections_dir, file_name)
        
        # Write section file
        with open(section_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(clean_content))
        
        # Get file size
        file_size = get_file_size(section_file)
        
        # Add to index with enhanced information
        index["sections"].append({
            'section': section_num,
            'title': section_title,
            'page_start': page_range['start_page'],
            'page_end': page_range['end_page'],
            'txt_filename': f"sections/{file_name}",
            'size': file_size
        })
        
        print(f"Processed section {section_num} (pages: {page_range['start_page']} to {page_range['end_page']})")
    
    # Write the index file (in the output directory, not the sections directory)
    index_file = os.path.join(output_dir, 'index.json')
    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2)
    
    # Create README.md with table of contents
    readme_content = create_readme(index, sections_dir)
    readme_file = os.path.join(output_dir, 'README.md')
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"File processed and split into sections in {output_dir}")
    print(f"Index file created: {index_file}")
    print(f"README.md created: {readme_file}")
    print(f"Total sections processed: {len(section_content)}")
    print(f"TPR revision date: {revision_date}")

if __name__ == "__main__":
    main()