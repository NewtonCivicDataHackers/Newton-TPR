# Setting Up Cron Job for TPR Updates

This document explains how to set up a cron job to automatically check for and process updates to the Newton Traffic and Parking Regulations document.

## Overview

The `update-tpr-cron.sh` script performs the following tasks:
1. Downloads the latest TPR document from Newton's website
2. Checks if the revision date has changed
3. If there's a new revision, processes the document
4. Optionally commits and pushes changes to git

## Requirements

- Linux or macOS system with cron
- Python 3.8 or later
- Git (if using the git commit functionality)
- Required Python packages installed (`requests`, `beautifulsoup4`, `pdfminer.six`)

## Installation Steps

### 1. Install Python Dependencies

Run the following commands in the repository directory:

```bash
# Using pip
pip install requests beautifulsoup4 pdfminer.six

# Or using uv
uv pip install requests beautifulsoup4 pdfminer.six
```

### 2. Configure the Script

The script has several configurable variables at the top:

- `REPO_DIR`: Automatically determined, but you can override it
- `TEMP_DIR`: Directory for temporary files
- `GIT_COMMIT`: Whether to commit changes to git (default: true)
- `LOG_FILE`: Path to the log file

### 3. Test the Script

Before setting up the cron job, make sure the script works correctly:

```bash
./scripts/update-tpr-cron.sh
```

Check the console output and the log file for any errors.

### 4. Set Up the Cron Job

#### For a user crontab:

```bash
crontab -e
```

Add a line like this to run the script every Monday at 8:00 AM:

```
0 8 * * 1 /full/path/to/newton-tpr/scripts/update-tpr-cron.sh
```

#### For a system crontab:

```bash
sudo vim /etc/cron.d/tpr-update
```

Add a line like this:

```
0 8 * * 1 username /full/path/to/newton-tpr/scripts/update-tpr-cron.sh
```

Replace `username` with the appropriate user account.

### 5. Environment Variables (if needed)

If the cron environment doesn't have the necessary environment variables (like PATH), you might need to add them:

```
0 8 * * 1 PATH=/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin HOME=/home/username /full/path/to/newton-tpr/scripts/update-tpr-cron.sh
```

## Disabling Git Operations

If you don't want the script to commit changes to git, you can disable this feature:

```bash
GIT_COMMIT=false ./scripts/update-tpr-cron.sh
```

Or modify the cron entry:

```
0 8 * * 1 GIT_COMMIT=false /full/path/to/newton-tpr/scripts/update-tpr-cron.sh
```

## Log Rotation

The script logs to a file named `tpr-update.log` in the repository root. Consider setting up log rotation to prevent this file from growing too large:

```bash
sudo vim /etc/logrotate.d/tpr-update
```

Add the following:

```
/full/path/to/newton-tpr/tpr-update.log {
    weekly
    rotate 4
    compress
    missingok
    notifempty
}
```

## Troubleshooting

- Check the log file for error messages
- Ensure the script has execute permission: `chmod +x scripts/update-tpr-cron.sh`
- Make sure the user running the cron job has write permission to the repository directory
- Check cron's mail for any error messages: `mail` or `/var/mail/username`