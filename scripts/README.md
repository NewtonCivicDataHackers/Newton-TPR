# TPR Processing Scripts

This directory contains scripts for processing the Newton Traffic and Parking Regulations (TPR) documents.

## process-tpr.py

This script processes a TPR document (PDF or text), extracts the revision date, and splits it into individual section files with a structured index.

### Dependencies

The script uses [PEP 723](https://peps.python.org/pep-0723/) to specify its dependencies:
- Python 3.8 or later
- pdfminer.six (for PDF processing)

### Usage

The recommended way to run the script is with [uv](https://github.com/astral-sh/uv):

```bash
uv run process-tpr.py path/to/tpr.pdf output-directory/
```

You can also run it directly if you have the dependencies installed:

```bash
./process-tpr.py path/to/tpr.pdf output-directory/
```

### Options

- `--save-text`: Save the intermediate text file after PDF conversion
- `--overwrite`: Overwrite existing directory if a directory with the same date already exists

### Example

```bash
uv run process-tpr.py ../tpr-revisions/2025-03-06/tpr.pdf ../tpr-revisions
```

### Output Structure

The script creates a directory structure based on the revision date extracted from the document:

```
output-directory/
└── YYYY-MM-DD/               # Directory named with the revision date
    ├── index.json            # Index file with section metadata
    ├── tpr.pdf               # Copy of the input PDF
    └── sections/             # Directory containing all section files
        ├── 00-preamble.txt   # Preamble content
        ├── 83.txt            # Section 83 content
        ├── 84.txt            # Section 84 content
        └── ...               # Additional section files
```

### Index.json Structure

The script generates an index.json file with the following structure:

```json
{
  "source": "tpr.pdf",
  "revision_date": "YYYY-MM-DD",
  "sections": [
    {
      "section": "83",
      "page_start": 1,
      "page_end": 3,
      "txt_filename": "sections/83.txt"
    },
    ...
  ]
}
```

### How It Works

1. Extracts the revision date from phrases like "Updated through December 20, 2024"
2. Converts the PDF to text using pdfminer
3. Detects page boundaries using form feed characters
4. Identifies section boundaries based on "Sec. TPR-XX." headers
5. Determines which pages contain the start and end of each section
6. Extracts and cleans the content for each section
7. Creates a directory structure based on the revision date
8. Writes individual section files and a structured index

## get-tpr.py

This script downloads the latest Newton Traffic and Parking Regulations document from the city's website.

### Dependencies

The script uses [PEP 723](https://peps.python.org/pep-0723/) to specify its dependencies:
- Python 3.8 or later
- requests (for HTTP requests)
- beautifulsoup4 (for HTML parsing)

### Usage

The recommended way to run the script is with [uv](https://github.com/astral-sh/uv):

```bash
uv run get-tpr.py output-file.pdf
```

You can also run it directly if you have the dependencies installed:

```bash
./get-tpr.py output-file.pdf
```

### Options

- `--url`: URL to the Newton Transportation Division page (default: https://www.newtonma.gov/government/public-works/transportation-division)
- `--direct-url`: Direct URL to the TPR PDF if known (bypasses searching the transportation page)
- `--cookie`: Cookie in format name=value. Can be specified multiple times for multiple cookies
- `--referer`: Referer URL to use in request headers

### Example

```bash
# Standard usage to fetch latest TPR
uv run get-tpr.py ../tpr-revisions/latest.pdf

# Using a direct URL
uv run get-tpr.py ../tpr-revisions/latest.pdf --direct-url "https://www.newtonma.gov/home/showpublisheddocument/xyz"

# Setting a specific referer and cookies
uv run get-tpr.py ../tpr-revisions/latest.pdf --referer "https://www.google.com" --cookie "name1=value1" --cookie "name2=value2"
```

### How It Works

1. Visits the Newton Transportation Division page
2. Searches for links containing "Traffic and Parking Regulations (TPR)"
3. Follows the link to download the PDF document
4. Saves the PDF to the specified output file

## Other Scripts

### tpr-to-sections.py
Converts a TPR document to individual section files with "section-" prefix.

### split_sections.py
A text-based TPR section splitter that processes documents with form feed characters.

### number-pages.sh
A shell script that adds page number markers to PDF files.