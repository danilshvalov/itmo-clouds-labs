from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os


class ISUParser:
    def __init__(self, profile_path, username, password, files_number, url):
        self.profile_path = profile_path
        self.username = username
        self.password = password
        self.files_number = files_number
        self.url = url
        self.driver = None

    def setup_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument(f'user-data-dir={self.profile_path}')
        prefs = {
            "download.default_directory": "/home/roman/University/Diploma/pars/docs",
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        }
        options.add_experimental_option("prefs", prefs)

        self.driver = webdriver.Chrome(options=options)

    def login(self):
        self.driver.get(self.url)
        try:
            username_input = self.driver.find_element(By.NAME, 'username')
            password_input = self.driver.find_element(By.NAME, 'password')

            username_input.send_keys(self.username)
            password_input.send_keys(self.password)

            login_button = self.driver.find_element(
                By.XPATH, '/html/body/div/div/div[1]/div/div[2]/form/div[4]/input[2]')
            login_button.click()
        except Exception as e:
            print('Already authorized')

    def download_files(self):
        time.sleep(5)
        for i in range(1, self.files_number + 1):
            xpath = f'/html/body/form/div[3]/div[3]/div[4]/div[1]/div/ajax_p_diss_list/div/div[3]/div/div[4]/table/tbody/tr[{i}]/td[5]/div/a'
            try:
                link = self.driver.find_element(By.XPATH, xpath)
                file_url = link.get_attribute('href')

                self.driver.get(file_url)
                time.sleep(2)

            except Exception as e:
                print(f'Error downloading file {i}')

    def quit(self):
        time.sleep(10)
        if self.driver:
            self.driver.quit()


if __name__ == "__main__":
    PROFILE_PATH = '.config/google-chrome'
    USERNAME = os.getenv("parser_username")
    PASSWORD = os.getenv("parser_password")
    FILES_NUMBER = 144
    URL = "https://isu.ifmo.ru/pls/apex/f?p=2143:7:112615017151226::NO:RP:DISS_ACTION,DISS_TYPE,DISS_YEAR,DISS_FACULTY,DISS_KAFEDRA:structure,bak,2024,725,all"

    parser = ISUParser(PROFILE_PATH, USERNAME, PASSWORD, FILES_NUMBER, URL)
    parser.setup_driver()
    parser.login()
    parser.download_files()
    parser.quit()
