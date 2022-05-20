from io import StringIO
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from sys import exit
from information import *
from time import sleep
from random import randint
from datetime import timedelta, datetime

# region functions

def check_time_and_select_group():
    '''check datetime and select group (create full_url) for send message'''
    day = datetime.today().strftime('%A')
    time = datetime.today().time()
    global full_url

    # شنبه
    if day == 'Saturday':
       # تولید محتوا
        full_url = 'attendance'
    # یکشنبه
    elif day == 'Sunday':
        # راه اندازی سیستم
        full_url = 'attendance'
    # دوشنبه
    elif day == 'Monday':
        if time.hour == 8 and time.minute == 0:
            # زبان
            full_url = baseurl + zaban
        elif time.hour == 8 and time.minute == 30:
            # زبان
            full_url = 'duplicate'
        elif time.hour == 9 and time.minute == 15:
            # عربی
            full_url = baseurl + arabi_din_va_zendegi
        elif time.hour == 9 and time.minute == 45:
            # دانش فنی پایه
            full_url = baseurl + danesh_fani_shabake
        elif time.hour == 10 and time.minute == 30:
            # دانش فنی پایه
            full_url = 'duplicate'
        elif time.hour == 11 and time.minute == 0:
            # دانش فنی پایه
            full_url = 'duplicate'
        elif time.hour == 11 and time.minute == 45:
            # الزامات
            full_url = 'duplicate'
        elif time.hour == 12 and time.minute == 15:
            # الزامات
            full_url = 'duplicate'
    # سه شنبه
    elif day == 'Tuesday':
        if time.hour == 8 and time.minute == 0:
            # فیزیک
            full_url = baseurl + fizik
        elif time.hour == 8 and time.minute == 30:
            # فیزیک
            full_url = 'duplicate'
        elif time.hour == 9 and time.minute == 15:
            # ریاضی
            full_url = baseurl + riazi
        elif time.hour == 9 and time.minute == 45:
            # ریاضی
            full_url = 'duplicate'
        elif time.hour == 10 and time.minute == 30:
            # نقشه کشی
            full_url = baseurl + naghshe_keshi
        elif time.hour == 11 and time.minute == 0:
            # نقشه کشی
            full_url = 'duplicate'
        elif time.hour == 11 and time.minute == 45:
            # نقشه کشی
            full_url = 'duplicate'
        elif time.hour == 12 and time.minute == 15:
            # نقشه کشی
            full_url = 'duplicate'
    # چهار شنبه
    elif day == 'Wednesday':
        if time.hour == 8 and time.minute == 0:
            # فارسی
            full_url = baseurl + farsi
        elif time.hour == 8 and time.minute == 30:
            # فارسی
            full_url = 'duplicate'
        elif time.hour == 9 and time.minute == 15:
            # جغرافی
            full_url = baseurl + joghrafia
        elif time.hour == 9 and time.minute == 45:
            # جغرافی
            full_url = 'duplicate'
        elif time.hour == 10 and time.minute == 30:
            # دین
            full_url = baseurl + arabi_din_va_zendegi
        elif time.hour == 11 and time.minute == 0:
            # دین
            full_url = 'duplicate'
        elif time.hour == 11 and time.minute == 45:
            # تربیت
            full_url = baseurl + tarbiat_badani
        elif time.hour == 12 and time.minute == 15:
            # تربیت
            full_url = 'duplicate'


def logger(success,log_time = True,text = ''):
    time = datetime.now().strftime('%A = %H:%M:%S')
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = dir_path + '/log.txt'
    with open(file_path, 'a') as handle:
        if log_time:
            handle.write(f'{time}\t' + '-' * 15 + f'\t{str(success)}' + '-' * 15 +f'\t{str(text)}\n')
    
def is_exist_element_xpath(driver,xpath):
    try:
        element = driver.find_element_by_xpath(xpath)
        return True
    except:
        return False

def send_message(driver: webdriver.Chrome):
    '''get group page and find field and fill it and in finally click send button'''

    while driver.current_url != full_url:
        driver.get(full_url)
        driver.refresh()
        sleep(3)
    # if page loading so we wait here until to done
    # if take very long time, we stop program because internet is not connect.
    second_of_wait = 0
    while is_exist_element_xpath(driver,loading_xpath):
            if second_of_wait == 80:
                logger(False,False,'No internet connection')
                driver.__exit__()
                exit()
            sleep(4)
            second_of_wait += 4
  
    # fill message field
    field = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, message_field_xpath)))
    field.send_keys(message)
    # send message
    send_button = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, send_button_xpath)))
    send_button.click()
    sleep(1.5)
    logger(True,text=message)

# endregion


# fill full_url variable (select group)
check_time_and_select_group()    


# no class time, so send message to save messages
if full_url == 'duplicate'  :
    # full_url = baseurl + 'u03itr02aa645ddef10466575438388a'
    # message = 'duplicate'
    # send_done = False
    logger(False,text='Duplicate')
    exit(0)
elif full_url == 'attendance':
    # full_url = baseurl + 'u03itr02aa645ddef10466575438388a'
    # message = 'attendance'
    # send_done =False
    logger(False,text='Attendance')
    exit(0)
elif full_url is None or full_url.strip() == '':
    # full_url = baseurl + 'u03itr02aa645ddef10466575438388a'
    # message = 'no class time'
    # send_done = False
    logger(False,text='No class time')
    exit(0)



# create a random delay time for send message (second)
random_delay_time = timedelta(minutes=randint(0, 2)).seconds

# delay
sleep(random_delay_time)

chrome_options = webdriver.ChromeOptions()
#chrome_options.headless = True
chrome_options.add_argument(
    '--user-data-dir=/home/me/.config/google-chrome/')
chrome_options.add_argument(r'--profile-directory=Profile 1')
driver = webdriver.Chrome(
    executable_path='/usr/bin/chromedriver', options=chrome_options)
driver.get(baseurl)
# send message

send_message(driver)

# exit the driver
driver.__exit__()
