from typing import KeysView
from selenium import webdriver
from time import sleep
from textwrap import indent, wrap
from re import sub
from random import randint
from datetime import timedelta

baseurl = 'https://play.typeracer.com/'
start_button_css = 'a.bkgnd-green:nth-child(1)'
text_area_xpath = '/html/body/div[1]/div/div[1]/div/div[1]/div[1]/table/tbody/tr[2]/td[2]/div/div[1]/div/table/tbody/tr[2]/td[3]/table/tbody/tr[2]/td/table/tbody/tr[1]/td/table/tbody/tr[1]/td/div/div'
type_area_css = '.txtInput'
race_again_button_css = '#gwt-uid-20 > table > tbody > tr:nth-child(3) > td > table > tbody > tr > td:nth-child(2) > a'
conter_to_race_css = 'body > div.countdownPopup.horizontalCountdownPopup > div > table > tbody > tr > td > table > tbody > tr'
wpm_css = '#gwt-uid-20 > table > tbody > tr:nth-child(1) > td > table > tbody > tr:nth-child(2) > td > div > div > div > table:nth-child(1) > tbody > tr > td.rankPanelContainer > div > div.rankPanelWpm.rankPanelWpm-self'

def main():
    web_driver = initial_chrome()
    web_driver.get(baseurl)
    while not is_exist_element_css(web_driver,start_button_css):
        sleep(1)
    element = web_driver.find_element_by_css_selector(start_button_css)
    web_driver.execute_script("arguments[0].click();", element)

    
    while 1 :
        text = get_text(web_driver)
        type_text(web_driver,text)
        type_race_again(web_driver,race_again_button_css)

def type_race_again(driver:webdriver.Chrome,again_button_css):
    while not is_exist_element_css(driver,again_button_css):
        sleep(1)
    again_button = driver.find_element_by_css_selector(again_button_css)
    driver.execute_script("arguments[0].click();", again_button)


def is_exist_element_css(driver:webdriver.Chrome,css):
    try:
        element = driver.find_element_by_css_selector(css)
        return True
    except:
        return False

def get_text(driver:webdriver.Chrome):
    text = ''
    sleep(0.5)
    text_area = driver.find_element_by_xpath(text_area_xpath)
    childs = text_area.find_elements_by_tag_name('span')

    counter = 1
    for item in childs:
        letters = (item.text)
        text += letters
        if counter == len(childs) -1 :
            text += ' '
        counter += 1

    return text

def type_text(driver:webdriver.Chrome,text:str):
    while not is_exist_element_css(driver,type_area_css):
        sleep(1)
    type_area = driver.find_element_by_css_selector(type_area_css)
    
    text_word_list= text.split()
    text_legnth = len(text_word_list) - 1
    
    index = 0
    while(index <= text_legnth):
        for t in text_word_list:
            if not text_word_list[index + 1] == ',':
                text_word_list[index] = t + ' '

    while is_exist_element_css(driver,conter_to_race_css):
        sleep(1)
    
    for t in text_word_list:
        # i'm not cheeating (:
        random_delay_time =  randint(0, 9)
        micro_second = float(f'0.{random_delay_time}')
        sleep(micro_second)
        if is_exist_element_css(driver,wpm_css):
            wpm = int(driver.find_element_by_css_selector(wpm_css).text[0:-3])
            if wpm > 99 :
                sleep(1.4)
        type_area.send_keys(t)
    

    # counter = 0
    # for t in text_array:
    #     if counter != 0 :
    #         t = ' ' + t
    #     type_area.send_keys(t)
    #     counter += 1


def initial_chrome():
    chrome_options = webdriver.ChromeOptions()
    #chrome_options.headless = True
    chrome_options.add_argument(
        '--user-data-dir=/home/me/.config/google-chrome/')
    chrome_options.add_argument(r'--profile-directory=Profile 1')
    driver = webdriver.Chrome(
        executable_path='/usr/bin/chromedriver', options=chrome_options)
    return driver







if __name__ == '__main__':
    main()