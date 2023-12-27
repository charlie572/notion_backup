import os
import re
import shutil
from configparser import ConfigParser
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

    # click download button
    download_button = driver.find_element(by=By.XPATH, value="//*[text()='Download']")
    download_button.click()


def move_notion_export(destination):
    downloads_folder = os.path.expanduser("~/Downloads")
    pattern = re.compile(r"[0-9a-f\-]+_Export[0-9a-f\-]+\.zip")
    for dir_entry in os.scandir(downloads_folder):
        if pattern.match(dir_entry.name):
            break
    else:
        raise RuntimeError

    shutil.move(dir_entry.path, destination)


def main():
    parser = ConfigParser()
    parser.read("config.ini")

    # instantiate driver
    options = Options()
    options.binary = FirefoxBinary(parser.get("firefox", "executable"))
    options.profile = FirefoxProfile(parser.get("firefox", "profile"))
    driver = webdriver.Firefox(options=options)

    start_notion_export(driver)
    driver.close()
    sleep(60 * 20)

    driver = webdriver.Firefox(options=options)
    download_notion_export(driver)
    driver.close()
    sleep(60 * 5)

    move_notion_export(parser.get("exports", "directory"))


if __name__ == "__main__":
    main()
