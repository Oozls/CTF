# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from threading import Thread
from difflib import SequenceMatcher
import os, time, json

class Main():
    def __init__(self):
        # Setting Location #
        self.dir_path = os.path.split(__file__)[0]
        self.record_path = os.path.join(self.dir_path, 'record.json')

        # Setting Url and Keyword #
        self.df_url = 'https://www.roblox.com/discover/?Keyword='
        self.keyword = input('Type Keyword... ').strip()
        self.full_url = self.df_url + self.keyword

        # Setting Html Searching Time #
        self.hst = input('Type Html Searching Time... ')
        if not self.hst.isdigit(): # hst isn't a number #
            print('Unexpected \'hst\' Found')
            os.system('pause')
        else:
            self.hst = int(self.hst)
        
        # Setting Options #
        self.options = {}

        only_korean = input('Record Only Korean? Y/N ')
        if only_korean.strip() == 'Y' or only_korean.strip() == 'y':
            only_korean = True
        else:
            only_korean = False
        self.options['ok'] = only_korean

        remove_tower = input('Remove Tower or 타워? Y/N ')
        if remove_tower.strip() == 'Y' or remove_tower.strip() == 'y':
            remove_tower = True
        else:
            remove_tower = False
        self.options['rt'] = remove_tower

        ratio = input('Type Overrap Ratio (0 to 100) ... ')
        if not ratio.isdigit(): # ratio isn't a number #
            print('Unexpected \'ratio\' Found')
            os.system('pause')
        else:
            ratio = float(ratio)/100
        self.options['ratio'] = ratio
        
        # Calling Class WebDriver #
        global source
        self.webdriver = WebDriver(self.full_url, self.hst)

        self.record()
    
    def restrict_string(self, text):
        def ok(str1):
            new_text = ''
            for letter in str1:
                if ord('가') <= ord(letter) <= ord('힣'):
                    new_text = new_text + letter
            return new_text     

        def rt(str2):
            str2 = str2.replace('Tower','')
            str2 = str2.replace('TOWER','')
            str2 = str2.replace('타워','')
            return str2
        
        if self.options['ok']: text = ok(text)
        if self.options['rt']: text = rt(text)
        
        return text

    def record(self):
        global source
        self.record_data = {}
        self.source = BeautifulSoup(source, 'html.parser')
        self.elements = self.source.find_all(class_='grid-item-container game-card-container')

        for element in self.elements:

            div = element.find(class_='game-card-name game-name-title')
            div_text = self.restrict_string(div.text)

            if not div_text in self.record_data: # If the name is not in the data #
                
                found = False # It means whether there is similar name or not #
                found_name = ''
                for name in self.record_data:
                    if SequenceMatcher(None, div_text, name).ratio() > self.options['ratio']:
                        found = True
                        found_name = name
                        break
                
                if found:
                    self.record_data[found_name] += 1
                else:
                    self.record_data[div_text] = 1

        with open("record.json", "w", encoding='utf-8') as file:
            json.dump(self.record_data, file, indent=2, ensure_ascii=False)


class WebDriver():
    def __init__(self, url, hst):
        global source

        # Setting Variables #
        self.finished = False

        # Setting Driver #
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')

        self.driver = webdriver.Chrome(options=self.options)
        self.driver.get(url)
        print('Driver Booted')

        time.sleep(1)
        print('Driver Started')

        def count():
            time.sleep(hst)
            self.finished = True
            print('Html Searching Ended')
        t = Thread(target=count)
        t.start()

        # Scrolling Down #
        while not self.finished:
            self.driver.find_element(By.CLASS_NAME,'container-main').send_keys(Keys.END)
            time.sleep(.2)
            self.driver.find_element(By.CLASS_NAME,'container-main').send_keys(Keys.HOME)
            time.sleep(.2)
        print('Stopped Searching')

        time.sleep(3)
        
        # Getting Source #
        source = self.driver.page_source
        print('Got Html Source')

        time.sleep(3)

        self.driver.quit()
        print('Stopped Driver')


if __name__ == '__main__':
    main = Main()