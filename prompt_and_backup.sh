#!/bin/bash

# prompt user
confirm="$(dunstify "Notion Backup" "Run backup script?" -A yes,yes -A no,no)"

if [[ "$confirm" == "yes" ]] then
    # get new auth token
    echo "starting backup"
    source /home/charlie/git_repos/notion_backup/venv/bin/activate
    python /home/charlie/git_repos/notion_backup/backup.py
    deactivate

    echo "will download later"
    echo '/bin/bash /home/charlie/git_repos/notion_backup/prompt_and_backup.sh' | at now + 5 minute
else
    # schedule script to run later
    echo "will remind you later"
    echo '/bin/bash /home/charlie/git_repos/notion_backup/prompt_and_backup.sh' | at now + 1 hour
fi