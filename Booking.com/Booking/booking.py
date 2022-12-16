from selenium import webdriver
import os
import Booking.constants as const
from selenium.webdriver.common.by import By


class Booking(webdriver.Chrome):
    def __init__(self, driver_path=r"C:\SeleniumDrivers", teardown=False):
        self.driver_path =driver_path
        self.teardown = teardown
        os.environ['PATH'] = self.driver_path
        super(Booking, self).__init__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def land_first_page(self):
        self.get(const.BASE_URL)

    def currency(self):
        money = self.find_element(By.CSS_SELECTOR,'span[class="bui-button__text"]')
        money.click()
        select_other_currency = self.find_element(By.CSS_SELECTOR,'a[data-modal-header-async-url-param="changed_currency=1&selected_currency=USD&top_currency=1"]')
        select_other_currency.click()
