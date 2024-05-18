# Notion Backup

This script will back up Notion regularly. It checks if enough time has passed since the 
last backup, so you can run it often.

It works in two phases:
1. Click the "export all workspace content button".
2. Click the download button on the notification in Notion when it is done. Then move 
the export to the correct directory, and click the archive button on the notification.

The current phase is saved to state.json, so the script can resume the phase if it fails.

# Setup

You may need to download firefox from the website rather than using snap.

1. Clone repository.
2. Create virtual environment.
3. Install requirements.
5. Create a new firefox profile by opening about:profiles in firefox, and sign in to Notion using it.
6. Copy the root directory of the profile on about:profiles. 
7. Create a config file using create_config.py, then fill in the settings in the file.
8. Run backup.py regularly.
