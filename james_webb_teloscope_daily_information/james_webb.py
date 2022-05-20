#!/usr/bin/env python3
from selenium import webdriver
from sys import argv
from smtplib import SMTP_SSL
from ssl import create_default_context
from datetime import datetime


def get_information():

    # launch_elapsed_xpath = '//*[@id="launchElapsedTime"]'
    # from_earth_xpath = '//*[@id="milesEarth"]'
    # to_l2_orbit_xpath = '//*[@id="milesToL2"]'
    # distance_complete_xpath = '//*[@id="percentageCompleted"]'
    # cruising_speed_xpath = '//*[@id="speedMi"]'
    hot_side_a_xpath = '//*[@id="tempWarmSide1F"]'
    hot_side_b_xpath = '//*[@id="tempWarmSide2F"]'
    cold_side_c_xpath = '//*[@id="tempCoolSide1F"]'
    cold_side_d_xpath = '//*[@id="tempCoolSide2F"]'
    MIRI_NIRCam_NirSpec_1 = '//*[@id="tempInstMiriF"]'
    MIRI_NIRCam_NirSpec_2 = '//*[@id="tempInstNirCamF"]'
    MIRI_NIRCam_NirSpec_3 = '//*[@id="tempInstNirSpecF"]'
    FGS_NIRISS_FSM_4 = '//*[@id="tempInstFsmF"]'
    FGS_NIRISS_FSM_5 = '//*[@id="tempInstFsmF"]'
    base_url = 'https://www.jwst.nasa.gov/content/webbLaunch/whereIsWebb.html'

    firefox_options = webdriver.FirefoxOptions()
    firefox_options.headless = False
    driver = webdriver.Firefox(options=firefox_options)
    print("Getting Information ...")
    try:
        # Wait maximum 40 seconds and then extract information from page
        driver.set_page_load_timeout(40)
        driver.get(base_url)
    except:
        pass

    time = datetime.now().strftime('%Y-%m-%d --- %H:%M:%S')

    information: dict = {
        "hot_side": {"a": '', "b": ''},
        "cold_side": {"c": '', "d": ''},
        "MIRI_NIRCam_NirSpec": {
            "1": driver.find_element_by_xpath(MIRI_NIRCam_NirSpec_1).text + 'F',
            "2": driver.find_element_by_xpath(MIRI_NIRCam_NirSpec_2).text + 'F',
            "3": driver.find_element_by_xpath(MIRI_NIRCam_NirSpec_3).text + 'F'
        },
        "FGS_NIRISS_FSM": {
            "4": driver.find_element_by_xpath(FGS_NIRISS_FSM_4).text + 'F',
            "5": driver.find_element_by_xpath(FGS_NIRISS_FSM_5).text + 'F',
        },
        "information_time": time
        # "from_earth": driver.find_element_by_xpath(from_earth_xpath).text + ' mi',
        # "to_l2_orbit": driver.find_element_by_xpath(to_l2_orbit_xpath).text +' mi',
        # "cruising_speed": driver.find_element_by_xpath(cruising_speed_xpath).text + ' mi/s',
        # "cruising_speed": driver.find_element_by_xpath(cruising_speed_xpath).text + ' mi/s',
        # "cruising_speed": driver.find_element_by_xpath(cruising_speed_xpath).text + ' mi/s',
        # "distance_complete": driver.find_element_by_xpath(distance_complete_xpath).text + "%",
    }
    information['hot_side']['a'] = driver.find_element_by_xpath(
        hot_side_a_xpath).text + ' F'
    information['hot_side']['b'] = driver.find_element_by_xpath(
        hot_side_b_xpath).text + ' F'
    information['cold_side']['c'] = driver.find_element_by_xpath(
        cold_side_c_xpath).text + ' F'
    information['cold_side']['d'] = driver.find_element_by_xpath(
        cold_side_d_xpath).text + ' F'

    driver.quit()
    return information


def send_information(msg, user_email):
    from_email = 'james.webb.daily.information@gmail.com'
    password = 'jameswebbdailyinformation'

    user_email = user_email
    context = create_default_context()

    try:
        with SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
            server.login(from_email, password)
            server.sendmail(from_email, [user_email], msg)
        return True
    except:
        return False


def log(message):
    with open('log.txt', 'a') as handle:
        handle.write(message + '\n')


def main():
    try:
        user_email = argv[1]
    except:
        user_email = None
        message = 'If you want this program send you "JAMES WEBB TELESCOPE" information to your email, please give your "Gmail" address with argument to program.'
        print(message)

    information = get_information()

    msg = \
    f'''
From: james.webb.daily.information@gmail.com
To: {user_email}
Subject: <James Webb Telescope Daily Information>
MIRI_NIRCam_NirSpec =
    1:{information['MIRI_NIRCam_NirSpec']['1']}
    2:{information['MIRI_NIRCam_NirSpec']['2']}
    3:{information['MIRI_NIRCam_NirSpec']['3']}
FGS_NIRISS_FSM =
    4:{information['FGS_NIRISS_FSM']['4']}
    5:{information['FGS_NIRISS_FSM']['5']}
Hot Side =
    a: {information['hot_side']['a']}
    b: {information['hot_side']['b']}
Cold Side =
    a: {information['cold_side']['c']}
    b: {information['cold_side']['d']}

Time = {information["information_time"]}
    '''

    if user_email != None:
        result = send_information(msg, user_email)
        time = datetime.now().strftime('%Y-%m-%d --- %H:%M:%S')
        if result:
            log(f'[{time}]   Email sent.')
        else:
            log(f'[{time}]   Email not sent.')
    else:
        msg = \
        f'''
MIRI/NIRCam/NirSpec:
    1: {information['MIRI_NIRCam_NirSpec']['1']}
    2: {information['MIRI_NIRCam_NirSpec']['2']}
    3: {information['MIRI_NIRCam_NirSpec']['3']}
FGS-NIRISS/FSM:
    4: {information['FGS_NIRISS_FSM']['4']}
    5: {information['FGS_NIRISS_FSM']['5']}
Hot Side:
    a: {information['hot_side']['a']}
    b: {information['hot_side']['b']}
Cold Side:
    a: {information['cold_side']['c']}
    b: {information['cold_side']['d']}

Time: {information['information_time']}
        '''
        print(msg)


if __name__ == '__main__':
    main()
