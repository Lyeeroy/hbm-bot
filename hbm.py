from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *
import time
import re

print('Number Memory [1]')
print('Reaction time [2]')
game = input('Game: ')
if game == '1':
    level_limit = input('Max level cap: ')
if game == '2':
    delay = (0.25)
    level_limit = input('Max tries cap: ')
loginQ = input('log in? (y/n): ')
if loginQ == "y":
    print('---------------------------')
    input_username = input('Username: ')
    input_password = input('Password: ')
    print('---------------------------')
elif loginQ == "auto":  # auto login
    input_username = "username"  # username
    input_password = "passw"  # passw

class hbm(object):
    def openChrome(self):
        self.driver = webdriver.Chrome()
        if loginQ == "y":
            hbm.login()
        elif loginQ == "auto":
            hbm.login()
        elif loginQ == "n":
            pass
        else:
            print('(y/n/auto)')
            quit()
        if game == "1":
            hbm.number_memory()
        if game == "2":
            hbm.reaction_time()
        else:
            quit()

    def login(self):
        self.driver.get("https://www.humanbenchmark.com/log_in")
        try:
            username = self.driver.find_element_by_id('username')
            username.send_keys(input_username)

            password = self.driver.find_element_by_id('password_plaintext')
            password.send_keys(input_password)

            loginbtn = self.driver.find_element_by_name("commit")
            loginbtn.click()
        except NoSuchElementException:
            print("wrong page?\n")
            quit()

        if self.driver.current_url == ('https://www.humanbenchmark.com/sessions'):
            print('invalid email or password')
            quit()

    def number_memory(self):
        self.driver.get("https://www.humanbenchmark.com/tests/number-memory")
        startbtn = self.driver.find_element_by_xpath("//a[@class='button start']")
        startbtn.click()
        print('------------')
        print('Game started:')
        print('------------')
        oldelement = 0
        while True:
            try:
                self.element = self.driver.find_element_by_xpath("//div[@class='big-number ng-binding']").text
            except NoSuchElementException:
                time.sleep(0.25)

            try:
                input_text = self.driver.find_element_by_xpath("//input[@type='text']")
                input_text.send_keys(self.element, Keys.ENTER)
            except NoSuchElementException:
                time.sleep(0.25)

            try:
                time.sleep(0.8)
                try:
                    self.lvl = self.driver.find_element_by_xpath("//span[@class='number ng-binding']").text
                    if oldelement != self.element:
                        print(self.element, '     (', self.lvl, '/', level_limit, ')')
                    oldelement = self.element
                    if self.lvl == level_limit:
                        break
                except NoSuchElementException:
                    pass
                startbtn = self.driver.find_element_by_xpath("//a[@class='button next-question']")
                startbtn.click()
            except NoSuchElementException:
                time.sleep(0.25)

    def reaction_time(self):
        self.driver.get("https://www.humanbenchmark.com/tests/reactiontime")
        startbtn = self.driver.find_element_by_xpath("//div[@class='test-wrapper ng-scope']")
        def RTmain():
            startbtn.click()
            while True:
                try:
                    clickstring = self.driver.find_element_by_xpath("//div[contains(text(),'Click!')]")
                    startbtn.click()
                except NoSuchElementException:
                    time.sleep(0.18)

#--------- GO FASTER OR SLOWER >> DEPENDS ON AVERAGE TIME ------ (UNFORTUNATELY DOESNT WORK CUZ WEBSITE IS TRASH)------------------------
                    #avg = self.driver.find_element_by_xpath("//div[@class='average ng-binding']").text #average time
                    #purge = int(re.search(r'\d+', avg).group())
                    #if purge < 100:
                    #    print(purge, ' < 100')
                    #    time.sleep(0.099999999999)
                    #elif purge > 100:
                    #    print(purge, ' > 100')
                    #    #time.sleep(0.2)
                    #elif purge == 100:
                    #    startbtn.click()
                    #    quit()
# --------------------------------------------------------------------------------------------------------------------------------------

                else:
                    break
        print('------------')
        print('Game started:')
        print('------------')
        for i in range(0, int(level_limit)):
            avg = self.driver.find_element_by_xpath("//div[@class='average ng-binding']").text #average time
            purge = int(re.search(r'\d+', avg).group())
            print(i+1, ' / ', level_limit, '     (Average time:', purge, ')')
            RTmain()


hbm = hbm()
hbm.openChrome()