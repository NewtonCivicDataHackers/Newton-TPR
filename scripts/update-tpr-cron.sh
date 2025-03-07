#!/bin/bash
#
# Cron script to check for updates to the Newton TPR document
# This script:
# 1. Downloads the latest TPR document
# 2. Checks if it has been updated
# 3. Processes it if needed
# 4. Optionally commits changes to git
#

set -e  # Exit on error

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

# Download the latest TPR document
log "Downloading latest TPR document..."
python scripts/get-tpr.py "$TEMP_PDF"

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

# Process the document if needed
if [ "$NEEDS_PROCESSING" = true ]; then
  log "Processing new TPR document with revision date $REVISION_DATE..."
  python scripts/process-tpr.py "$TEMP_PDF" "$REPO_DIR"
  log "Processing complete"
  
  # Commit changes if requested
  if [ "$GIT_COMMIT" = true ]; then
    log "Committing changes to git..."
    
    # Configure git if running from cron
    git config --local user.name "TPR Update Bot" || true
    git config --local user.email "tpr-bot@example.com" || true
    
    # Add all changed files
    git add index.json README.md sections/ tpr.pdf
    
    # Create a new tag for this revision
    TAG_NAME="tpr-$REVISION_DATE"
    
    # Commit with the revision date
    git commit -m "Update TPR to revision $REVISION_DATE" -m "Automatically updated by cron job"
    
    # Push the changes if we have a remote
    if git remote -v | grep -q origin; then
      log "Pushing changes to remote repository..."
      git push
      
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