#!/bin/bash

# prompt user
confirm="$(dunstify "Notion Backup" "Run backup script?" -A yes,yes -A no,no)"

if [[ "$confirm" == "yes" ]] then
    # run backup script
    source /home/charlie/git_repos/notion_backup/venv/bin/activate
    python /home/charlie/git_repos/notion_backup/backup.py
    deactivate

    notify-send "Notion Backup" "Running backup script."
    echo '/bin/bash /home/charlie/git_repos/notion_backup/prompt_and_backup.sh' | at now + 5 minute
else
    # schedule script to run later
    notify-send "Notion Backup" "Will remind you later."
    echo '/bin/bash /home/charlie/git_repos/notion_backup/prompt_and_backup.sh' | at now + 1 hour
fi