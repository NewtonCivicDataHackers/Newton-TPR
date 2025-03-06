#!/usr/bin/env python3

import os
import re
import sys
import json
import argparse

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

def process_file(input_file):
    """Process the input file to detect form feeds and page boundaries."""
    # Read the file as binary to properly handle form feed characters
    with open(input_file, 'rb') as f:
        content_bytes = f.read()
    
    # Convert bytes to a string and split by form feed character
    content_str = content_bytes.decode('utf-8', errors='replace')
    
    # Find all form feed positions
    form_feed_positions = []
    position = 0
    while True:
        position = content_str.find('\f', position)
        if position == -1:
            break
        form_feed_positions.append(position)
        position += 1
    
    # Create pages using form feed positions
    pages = []
    start_pos = 0
    
    for page_num, pos in enumerate(form_feed_positions, 1):
        page_content = content_str[start_pos:pos]
        pages.append({
            'page_number': page_num,
            'content': page_content.splitlines()
        })
        start_pos = pos + 1
    
    # Add the last page
    if start_pos < len(content_str):
        pages.append({
            'page_number': len(pages) + 1,
            'content': content_str[start_pos:].splitlines()
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
    start_line = None
    
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
    if current_section is not None and 'end_line' in section_boundaries[current_section] and section_boundaries[current_section]['end_line'] is None:
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
    parser = argparse.ArgumentParser(description='Split a TPR document into sections with accurate page ranges.')
    parser.add_argument('input_file', help='Input file to split')
    parser.add_argument('output_dir', help='Output directory for sections')
    args = parser.parse_args()

    input_file = args.input_file
    output_dir = args.output_dir

    # Check if input file exists
    if not os.path.isfile(input_file):
        print(f"Error: Input file '{input_file}' does not exist.")
        sys.exit(1)

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Process the input file to detect form feeds and page boundaries
    pages, processed_text = process_file(input_file)
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
    preamble_file = os.path.join(output_dir, '00-preamble.txt')
    with open(preamble_file, 'w') as f:
        f.write('\n'.join(preamble_lines))
    print(f"Created preamble file: {preamble_file}")
    
    # Extract and clean content for each section
    section_content = extract_section_content(processed_text, section_boundaries)
    
    # Create index data
    index = []
    
    # Process each section
    for section_num in sorted(section_content.keys(), key=int):
        section_lines = section_content[section_num]
        page_range = section_page_ranges.get(section_num, {'start_page': None, 'end_page': None})
        
        # Clean the section content
        clean_content = clean_section_content(section_lines)
        
        # Write section file
        section_file = os.path.join(output_dir, f"section-{section_num}.txt")
        with open(section_file, 'w') as f:
            f.write('\n'.join(clean_content))
        
        # Add to index
        index.append({
            'section': section_num,
            'page_start': page_range['start_page'],
            'page_end': page_range['end_page'],
            'filename': f"section-{section_num}.txt"
        })
        
        print(f"Processed section {section_num} (pages: {page_range['start_page']} to {page_range['end_page']})")
    
    # Write the index file
    index_file = os.path.join(output_dir, 'index.json')
    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2)
    
    print(f"File split into sections in {output_dir}")
    print(f"Index file created: {index_file}")
    print(f"Total sections processed: {len(section_content)}")

if __name__ == "__main__":
    main()