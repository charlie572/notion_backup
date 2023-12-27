from selenium import webdriver
from selenium.webdriver import FirefoxProfile
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options


def main():
    # instantiate driver
    options = Options()
    options.binary = FirefoxBinary("/snap/firefox/current/usr/lib/firefox/firefox")
    options.profile = FirefoxProfile("/home/charlie/snap/firefox/common/.mozilla/firefox/zcff3mio.Bot")
    driver = webdriver.Firefox(options=options)

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

    driver.close()


if __name__ == "__main__":
    main()
