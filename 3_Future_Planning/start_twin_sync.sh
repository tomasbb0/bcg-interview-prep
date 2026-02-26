#!/bin/bash

# --- TWIN FOLDER SYNC SCRIPT ---
# This script keeps your local "Cloud Free" folder synced to a Cloud folder automatically.

# 1. The "Master" Local Folder (Where you work)
SOURCE_DIR="/Users/tomasbatalha/Downloads/Tomas_Batalha_Future_Plan/"

# 2. The "Twin" Cloud Folder (Where the backup goes)
# AUTOMATICALLY CONFIGURED FOR iCLOUD DRIVE
DEST_DIR="/Users/tomasbatalha/Library/Mobile Documents/com~apple~CloudDocs/Professional/2 - My Stuff/Planning/Tomas_Batalha_Future_Plan_BACKUP"

echo "---------------------------------------------------"
echo "STARTING TWIN FOLDER SYNC"
echo "Master: $SOURCE_DIR"
echo "Twin:   $DEST_DIR"
echo "---------------------------------------------------"
echo "Press [CTRL+C] to stop syncing."

# Create destination if it doesn't exist
mkdir -p "$DEST_DIR"

# Loop forever to sync every 10 seconds
while true; do
    # rsync copies files from Source to Dest
    # -a: Archive mode (keeps permissions/dates)
    # -v: Verbose (shows what is being copied)
    # --delete: If you delete a file in Master, it deletes in Twin
    rsync -av --delete "$SOURCE_DIR" "$DEST_DIR" --exclude '.DS_Store' --exclude 'start_twin_sync.sh'
    
    # Wait 10 seconds before checking again
    sleep 10
done
