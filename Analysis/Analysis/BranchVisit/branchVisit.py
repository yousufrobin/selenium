from selenium import webdriver
import os
import BranchVisit.constants as const
import pandas as pd

class branchVisit(webdriver.Chrome):
    def __init__(self, driver_path=r"C:\SeleniumDrivers", teardown=False):
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ['PATH'] = self.driver_path
        super(branchVisit, self).__init__()

    # __exit__ controls shutdown of chrome. Otherwise Chorme will
    # shutdown in default.
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def land_first_page(self):
        self.get(const.BASE_URL)

    def log_in(self):
        username = self.find_element_by_id("email")
        password = self.find_element_by_id("password")
        submit = self.find_element_by_id("btn_submit")

        username.send_keys(const.USER_NAME)
        password.send_keys(const.ADD_PASS)
        submit.click()

    # how much of deposit card is issued
    def deposit_card(self):
        current_month = 6
        day = 1
        year = 2022
        months = current_month + 1

        deposit_card_amount = 0

        # the for loop below determines whether the month is 31 days or 30 days
        # besides whether it is Feb of Leap Year or not
        for month in range(1, months):
            if month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12:
                day2 = 31
            else:
                day2 = 30

            if month == 2:
                day2 = 28

            if month == 2 and year % 4 == 0:
                day2 = 29

            start_day = f"{day}-{month}-{year}"
            end_day = f"{day2}-{month}-{year}"

            # self.get(f"192.168.137.70/carddata/rep_adc_performance.php?txt_date1={day}-{month}-{year}&txt_date2={day2}-{month}-{year}&br_code={const.BRANCH}")


            self.get("http://192.168.137.70/carddata/rep_adc_performance_date.php")
            branch_code = self.find_element_by_id("br_code")
            start_date = self.find_element_by_id("txt_date1")
            start_date.clear()
            end_date = self.find_element_by_id("txt_date2")
            end_date.clear()
            submit = self.find_element_by_id("btn_submit")

            branch_code.send_keys(const.BRANCH)
            start_date.send_keys(start_day)
            end_date.send_keys(end_day)
            submit.click()

            deposit_card = self.find_element_by_xpath("/html/body/table/tbody/tr[4]/td/table/tbody/tr[3]/td[7]").text
            deposit_card_amount += int(deposit_card)

        print(deposit_card_amount)

    # compares the CRM Deposits with counter deposits
    def crm_deposit_rate(self):
        self.get(const.GB_URL)

        try:
            advanced = self.find_element_by_id("details-button")
            advanced.click()
            proceed = self.find_element_by_id("proceed-link")
            proceed.click()
        except:
            print("No need to select advance and proceed")

        username = self.find_element_by_id("user")
        password = self.find_element_by_id("password")
        branch = self.find_element_by_id("brCode")
        submit = self.find_element_by_class_name("login-button")

        username.send_keys(const.USER_NAME)
        password.send_keys(const.GB_PASS)
        branch.send_keys(const.BRANCH)
        submit.click()

        # the for loop below is to check and compare Account Type wise deposits
        report = []
        tab_num1 = 1
        accounts = ['option[value="03"]', 'option[value="02"]', 'option[value="01"]']
        for account in accounts:
            transaction_types = ['option[value="101"]', 'option[value="107"]']
            tab_num = tab_num1

            for transaction_type in transaction_types:
                self.execute_script("window.open('');")
                self.switch_to.window(self.window_handles[tab_num])

                self.get("https://192.168.36.86/gbreport/indexForRangeTransactions.do")

                account_type = self.find_element_by_name("accType")
                account_type.click()
                select_acc_type = self.find_element_by_css_selector(account)
                account_name = select_acc_type.text
                select_acc_type.click()

                counter_receive = self.find_element_by_name("trType")
                counter_receive.click()
                counter_receive_type = self.find_element_by_css_selector(transaction_type)
                deposit_type = counter_receive_type.text
                counter_receive_type.click()

                start_date = self.find_element_by_name("fromDate")
                start_date.clear()
                start_date.send_keys(const.year_first_day)
                html_selecting = self.find_element_by_css_selector('option[value="html"]')
                html_selecting.click()
                submit = self.find_element_by_class_name("button")
                submit.click()

                deposit_quantity = self.find_element_by_xpath('//td[last()-1]/a[last()]/table/tbody/tr[last()-3]/td[last()-3]/span').text
                deposit_amount = self.find_element_by_xpath('//a[last()]/table/tbody/tr[last()-3]/td[last()-2]/span').text


                temporary_data = {'Account Name': account_name,
                        'Deposit Type': deposit_type,
                        'Deposit Quantity': deposit_quantity,
                        'Deposit Amount': deposit_amount}

                report.append(temporary_data)


                tab_num += 1
                self.implicitly_wait(15)

            tab_num1 += 2

        # print(report)

        decorated_report = pd.DataFrame(report)

        print(decorated_report)