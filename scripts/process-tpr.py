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

def main():
    parser = argparse.ArgumentParser(description='Process a TPR document (PDF or text) and split it into sections.')
    parser.add_argument('input_file', help='Input PDF file to process')
    parser.add_argument('output_dir', help='Base directory to save processed files')
    parser.add_argument('--save-text', dest='save_text', action='store_true',
                        help='Save the intermediate text file after PDF conversion')
    parser.add_argument('--overwrite', dest='overwrite', action='store_true',
                        help='Overwrite existing directory if it already exists')
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
    
    # Create directory structure
    date_dir = os.path.join(args.output_dir, revision_date)
    sections_dir = os.path.join(date_dir, "sections")
    
    # Check if directory already exists and handle based on overwrite flag
    if os.path.exists(date_dir) and not args.overwrite:
        print(f"Error: Directory '{date_dir}' already exists.")
        print("Use --overwrite flag to overwrite existing directory.")
        sys.exit(1)
    
    # Create directories
    os.makedirs(sections_dir, exist_ok=True)
    
    # Copy PDF file to the date directory
    pdf_dest = os.path.join(date_dir, "tpr.pdf")
    shutil.copy2(args.input_file, pdf_dest)
    print(f"Copied PDF to: {pdf_dest}")
    
    # Save the text file if requested
    if args.save_text:
        text_file = os.path.join(date_dir, "tpr.txt")
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
        "sections": []
    }
    
    # Process each section
    for section_num in sorted(section_content.keys(), key=int):
        section_lines = section_content[section_num]
        page_range = section_page_ranges.get(section_num, {'start_page': None, 'end_page': None})
        
        # Clean the section content
        clean_content = clean_section_content(section_lines)
        
        # Create filename just with the section number
        file_name = f"{section_num}.txt"
        section_file = os.path.join(sections_dir, file_name)
        
        # Write section file
        with open(section_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(clean_content))
        
        # Add to index
        index["sections"].append({
            'section': section_num,
            'page_start': page_range['start_page'],
            'page_end': page_range['end_page'],
            'txt_filename': f"sections/{file_name}"
        })
        
        print(f"Processed section {section_num} (pages: {page_range['start_page']} to {page_range['end_page']})")
    
    # Write the index file (in the date directory, not the sections directory)
    index_file = os.path.join(date_dir, 'index.json')
    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2)
    
    print(f"File processed and split into sections in {date_dir}")
    print(f"Index file created: {index_file}")
    print(f"Total sections processed: {len(section_content)}")

if __name__ == "__main__":
    main()