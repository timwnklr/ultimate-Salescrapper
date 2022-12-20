from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
import numpy as np


class wlwBot:

    def __init__(self):

        # initialte empty data lists
        self.name_list = []
        self.number_list = []
        self.address_list = []
        self.infos_list = []
        self.website_list = []

        # initialate browser
        self.website = input("Hallo Johannes, gib URL ein: ")
        self.driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()))

    def run(self):
        self.driver.get(self.website)
        try:
            self.accept_cookies()
        except:
            pass

        end = False

        while end == False:
            try:
                for self.n in range(30):
                    navigateBool = True
                    try:
                        self.navigate_search()
                    except:
                        navigateBool = False
                    self.get_number()
                    self.get_addresse()
                    self.get_website()
                    self.get_name()
                    if navigateBool == True:
                        self.driver.back()
                    self.n = self.n + 1

                try:
                    self.navigate_next()
                except:
                    end = True

            except Exception as e:
                print(e)
                end = True

        data_dict = {'name': self.name_list, 'number': self.number_list,
                     'addresse': self.address_list, 'website': self.website_list}
        df = pd.DataFrame(data_dict, columns=[
                          'name', 'number', 'addresse', 'website'])
        df.to_csv('salesInfos.csv')
        df = pd.read_csv("salesInfos.csv")
        df['name'].replace('', np.nan, inplace=True)
        df.dropna(subset=['name'], inplace=True)
        df = df.drop_duplicates(subset='number', keep="first")  
        df.drop('Unnamed: 0', inplace=True, axis=1)
        df.to_excel("salesInfos.xlsx")  

    # Helper Functions
    # ------------------------------------------------------------------------------

    def accept_cookies(self):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            (By.LINK_TEXT, "Alle Cookies akzeptieren")))
        button_cookies = self.driver.find_element(
            By.LINK_TEXT, "Alle Cookies akzeptieren")
        button_cookies.click()

    def navigate_search(self):
            WebDriverWait(self.driver, 1).until(EC.presence_of_element_located(
                (By.XPATH, "//div[@class='container search-results']")))
            div_container = self.driver.find_element(
                By.XPATH, "//div[@class='container search-results']")
            div_company = div_container.find_element(
                By.XPATH, ".//div[@style='order:{};']".format(str(self.n)))
            link_company = div_company.find_element(
                By.XPATH, ".//a[@class='company-title-link']")
            link_company.click()


    def get_name(self):
        try:
            company_name = self.driver.find_element(
                By.XPATH, "//h1[@class='business-card__title text-xl font-metropolis tablet:text-3xl']").text
            self.name_list.append(company_name)

        except:
            self.name_list.append("")

    def get_number(self):
        try:
            button_phone = self.driver.find_element(
                By.XPATH, "//a[@class='vis-phone__button text-base text-link']")
            button_phone.click()
            company_number = self.driver.find_element(
                By.XPATH, "//a[@data-test='phone__number']").text
            self.number_list.append(company_number)

        except:
            self.number_list.append("")

    def get_addresse(self):
        try:
            addresse = self.driver.find_element(
                By.XPATH, "//div[@class='business-card__address mb-2 text-base tablet:text-lg']").text
            self.address_list.append(addresse)

        except:
            self.address_list.append("")

    def get_infos(self):
        try:
            infos = [node.text for node in self.driver.find_elements(
                By.XPATH('//div[@class="facts-and-figures__value"]'))]
            self.infos_list.append(infos)

        except:
            self.infos_list.append("")

    def get_website(self):
        try:
            website = self.driver.find_element(
                By.CSS_SELECTOR, "#location-and-contact__website").get_attribute("href")
            self.website_list.append(website)

        except:
            self.website_list.append("")

    def navigate_next(self):
        next_button = self.driver.find_element(By.XPATH, "//a[@rel='next']")
        next_button.click()
# ------------------------------------------------------------------------------
