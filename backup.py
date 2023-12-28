import json
import os
import re
import shutil
import zipfile
from configparser import ConfigParser
import datetime
from time import sleep

from selenium import webdriver
from selenium.webdriver import FirefoxProfile
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options


def start_notion_export(driver):
    # open notion
    driver.get("https://www.notion.so/login")

    driver.implicitly_wait(10.0)

    # open settings
    settings_icon = driver.find_element(by=By.CLASS_NAME, value="sidebarSettings")
    settings_icon.click()
    workspace_settings_icon = driver.find_element(by=By.CLASS_NAME, value="settings")
    workspace_settings_icon.click()

    # click export button
    export_button = driver.find_element(by=By.XPATH, value="//*[text()='Export all workspace content']")
    export_button.click()
    export_button_2 = driver.find_element(by=By.XPATH, value="//*[text()='Export']")
    export_button_2.click()


def download_notion_export(driver):
    # open notion
    driver.get("https://www.notion.so/login")

    driver.implicitly_wait(10.0)

    # open updates sidebar
    updates_icon = driver.find_element(by=By.CLASS_NAME, value="sidebarUpdates")
    updates_icon.click()

    # find download notifications
    notification_divs = driver.find_elements(
        by=By.XPATH,
        value="//article[./div/div/div/div[text()='Download']]",
    )

    if len(notification_divs) == 0:
        return False

    for notification_div in notification_divs:
        # find buttons
        download_button = notification_div.find_element(
            by=By.XPATH,
            value="//div[text()='Download']",
        )
        archive_button = notification_div.find_element(
            by=By.CLASS_NAME,
            value="archive",
        )

        # download and archive
        download_button.click()
        archive_button.click()

    return True


def move_notion_export(destination):
    downloads_folder = os.path.expanduser("~/Downloads")
    pattern = re.compile(r"[0-9a-f\-]+_Export[0-9a-f\-\(\)]+\.zip")
    success = False
    for dir_entry in os.scandir(downloads_folder):
        if not pattern.match(dir_entry.name):
            continue
        if not zipfile.is_zipfile(dir_entry.path):
            continue
        if zipfile.ZipFile(dir_entry.path).testzip() is not None:
            continue

        shutil.move(dir_entry.path, destination)
        success = True

    return success


def delete_old_notion_exports(directory, max_backups):
    # get exports ordered by date
    files = [d.path for d in os.scandir(directory)]
    files.sort(key=lambda f: os.path.getmtime(f))

    for file in files[:-max_backups]:
        os.remove(os.path.join(directory, file))


def main():
    parser = ConfigParser()
    parser.read("config.ini")

    with open("state.json", "r") as f:
        data = json.load(f)

    next_backup = datetime.datetime.fromtimestamp(data["next_backup"])
    state = data["state"]

    backup_interval = datetime.timedelta(
        days=parser.getint("backups", "backup_interval")
    )

    if datetime.datetime.now() < next_backup:
        print("Not time for backup yet.")
        return

    # instantiate driver
    options = Options()
    options.binary = FirefoxBinary(parser.get("firefox", "executable"))
    options.profile = FirefoxProfile(parser.get("firefox", "profile"))
    options.add_argument("--headless")

    if state == "idle":
        # start export
        print("Accessing notion")
        driver = webdriver.Firefox(options=options)
        start_notion_export(driver)
        print("Started export")

        # update state
        data["state"] = "exporting"
        with open("state.json", "w") as f:
            json.dump(data, f)

        return

    # download export
    print("Accessing Notion")
    driver = webdriver.Firefox(options=options)
    success = download_notion_export(driver)
    if not success:
        return
    print("Downloading")

    # move export
    moved = False
    while not moved:
        sleep(5)
        moved = move_notion_export(parser.get("exports", "directory"))

    # delete old data
    print("Deleting old data")
    delete_old_notion_exports(
        parser.get("exports", "directory"),
        parser.getint("exports", "num_to_keep"),
    )

    # update state
    data["state"] = "idle"
    data["next_backup"] = (datetime.datetime.now() + backup_interval).timestamp()
    with open("state.json", "w") as f:
        json.dump(data, f)

    print("Done.")


if __name__ == "__main__":
    main()
