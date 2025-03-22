import json
from configparser import ConfigParser
from datetime import datetime


def main():
    parser = ConfigParser()

    parser.add_section("firefox")
    parser.set("firefox", "profile", "/home/charlie/.mozilla/firefox/k8zmz994.Scripts")
    parser.set("firefox", "binary", "/snap/firefox/current/usr/lib/firefox/firefox")

    parser.add_section("exports")
    parser.set("exports", "directory", "/home/charlie/notion_backups")
    parser.set("exports", "num_to_keep", "5")

    parser.add_section("backups")
    parser.set("backups", "backup_interval", "3")

    with open("config.ini", "w") as f:
        parser.write(f)

    with open("state.json", "w") as f:
        json.dump(
            {"next_backup": datetime.now().timestamp(), "state": "idle"},
            f,
        )


if __name__ == "__main__":
    main()
