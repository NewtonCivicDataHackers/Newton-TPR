#!/bin/bash
#
# Cron script to check for updates to the Newton TPR document
# This script:
# 1. Downloads the latest TPR document
# 2. Checks if it has been updated
# 3. Processes it if needed
# 4. Optionally commits changes to git
#
# Options:
#   --overwrite: Force processing even if the document hasn't changed
#

set -e  # Exit on error

# Parse command line arguments
FORCE_OVERWRITE=false
for arg in "$@"; do
  case $arg in
    --overwrite)
      FORCE_OVERWRITE=true
      shift
      ;;
    *)
      # unknown option
      ;;
  esac
done

# Configuration
REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"  # Repository root directory
TEMP_DIR="${REPO_DIR}/tmp"                    # Temporary directory for downloads
TEMP_PDF="${TEMP_DIR}/latest.pdf"             # Temporary PDF file
GIT_COMMIT=${GIT_COMMIT:-true}                # Whether to commit changes to git
LOG_FILE="${REPO_DIR}/tpr-update.log"         # Log file

# Make sure log directory exists
mkdir -p "$(dirname "$LOG_FILE")"

# Function to log messages
log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

# Create temp directory
mkdir -p "$TEMP_DIR"

# Change to the repository directory
cd "$REPO_DIR"

log "Starting TPR update check"

# Source URLs for Newton TPR
SOURCE_WEBPAGE="https://www.newtonma.gov/government/public-works/transportation-division"
SOURCE_PDF_URL=""  # Will be detected during download

# Download the latest TPR document
log "Downloading latest TPR document..."
DOWNLOAD_OUTPUT=$(python scripts/get-tpr.py "$TEMP_PDF")
log "Download complete"

# Try to extract the PDF URL from the download output
if echo "$DOWNLOAD_OUTPUT" | grep -q "Found TPR document link:"; then
    SOURCE_PDF_URL=$(echo "$DOWNLOAD_OUTPUT" | grep "Found TPR document link:" | sed 's/.*Found TPR document link: //')
    log "Detected PDF URL: $SOURCE_PDF_URL"
fi

if [ ! -f "$TEMP_PDF" ]; then
  log "Error: Failed to download TPR document"
  exit 1
fi

# Extract the revision date
log "Extracting revision date..."
REVISION_DATE=$(python scripts/process-tpr.py "$TEMP_PDF" "$TEMP_DIR" --extract-date-only | tail -n 1)
log "Detected revision date: $REVISION_DATE"

# Check if we need to process the document
if [ -f "index.json" ]; then
  CURRENT_REVISION=$(grep -o '"revision_date": *"[^"]*"' index.json | cut -d'"' -f4)
  log "Current revision date in repository: $CURRENT_REVISION"
  
  if [ "$CURRENT_REVISION" = "$REVISION_DATE" ]; then
    log "This revision ($REVISION_DATE) already exists in our repository - no updates needed"
    NEEDS_PROCESSING=false
  else
    log "New revision ($REVISION_DATE) detected (current is $CURRENT_REVISION)!"
    NEEDS_PROCESSING=true
  fi
else
  log "No existing index.json found - will process new document"
  NEEDS_PROCESSING=true
fi

# Check if we need to process the document based on revision date or force flag
if [ "$NEEDS_PROCESSING" = true ] || [ "$FORCE_OVERWRITE" = true ]; then
  if [ "$FORCE_OVERWRITE" = true ]; then
    log "Forcing processing with overwrite flag, even though revision date is unchanged..."
  else
    log "Processing new TPR document with revision date $REVISION_DATE..."
  fi
  
  # Process with source URLs
  SOURCE_ARGS=""
  if [ -n "$SOURCE_WEBPAGE" ]; then
    SOURCE_ARGS="$SOURCE_ARGS --source-url '$SOURCE_WEBPAGE'"
  fi
  if [ -n "$SOURCE_PDF_URL" ]; then
    SOURCE_ARGS="$SOURCE_ARGS --pdf-url '$SOURCE_PDF_URL'"
  fi
  
  # Add overwrite flag if forcing
  if [ "$FORCE_OVERWRITE" = true ]; then
    SOURCE_ARGS="$SOURCE_ARGS --overwrite"
  fi
  
  # Use eval to properly handle the quoted arguments
  eval "python scripts/process-tpr.py '$TEMP_PDF' '$REPO_DIR' $SOURCE_ARGS"
  log "Processing complete"
  
  # Commit changes if requested
  if [ "$GIT_COMMIT" = true ]; then
    log "Committing changes to git..."
    
    # Configure git if running from cron
    git config --local user.name "TPR Update Bot" || true
    git config --local user.email "tpr-bot@example.com" || true
    
    # Add all changed files
    git add index.json README.md sections/ tpr.pdf
    
    # Set commit message based on what we did
    if [ "$FORCE_OVERWRITE" = true ] && [ "$NEEDS_PROCESSING" = false ]; then
      # Only updated README or metadata, not a new revision
      COMMIT_MSG="Update README and metadata for TPR revision $REVISION_DATE"
      COMMIT_DESC="Forced update without revision change"
    else
      # New revision or first processing
      COMMIT_MSG="Update TPR to revision $REVISION_DATE"
      COMMIT_DESC="Automatically updated by cron job"
    fi
    
    # Create a new tag for this revision
    TAG_NAME="tpr-$REVISION_DATE"
    
    # Commit with the appropriate message
    git commit -m "$COMMIT_MSG" -m "$COMMIT_DESC"
    
    # Push the changes if we have a remote
    if git remote -v | grep -q origin; then
      log "Pushing changes to remote repository..."
      git push
      
      # Delete existing tag if we're using overwrite and the tag exists
      if [ "$FORCE_OVERWRITE" = true ] && git tag | grep -q "$TAG_NAME"; then
        log "Deleting existing tag $TAG_NAME for overwrite..."
        git tag -d "$TAG_NAME"
        git push origin :refs/tags/"$TAG_NAME" || true
      fi
      
      # Create and push a tag for this revision
      git tag -a "$TAG_NAME" -m "TPR revision $REVISION_DATE"
      git push origin "$TAG_NAME"
    else
      log "No remote repository configured, skipping push"
    fi
    
    log "Git operations completed successfully"
  fi
else
  log "No processing needed"
fi

# Clean up
log "Cleaning up..."
rm -rf "$TEMP_DIR"

log "TPR update check completed successfully"