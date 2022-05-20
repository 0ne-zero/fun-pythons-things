from requests import get
from bs4 import BeautifulSoup
from telethon.sync import TelegramClient
from telethon.tl.types import InputMessagesFilterMusic
import bs4
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

def iran_pro_league_standing():
    url = 'https://www.eurosport.com/football/iran-pro-league/standing.shtml'
    content = get(url)
    bs = BeautifulSoup(content.content)
    tbody = bs.find('tbody')

    # result/standing
    list_of_teams = [[]]

    for row in tbody.findChildren('tr'):

        team_information = {'name': '', 'position': '',
                            'play': '', 'wins': '', 'draws': '',
                            'loses': '', 'point': ''}

        counter = 1
        useless_cells_number = [3, 8, 9, 10]
        for cell in row.contents:
            if counter in useless_cells_number:
                counter += 1
                continue
            else:
                if counter == 1:
                    team_information['position'] = cell.text
                elif counter == 2:
                    team_information['name'] = cell.text
                elif counter == 4:
                    team_information['play'] = cell.text
                elif counter == 5:
                    team_information['wins'] = cell.text
                elif counter == 6:
                    team_information['draws'] = cell.text
                elif counter == 7:
                    team_information['loses'] = cell.text
                elif counter == 11:
                    team_information['point'] = cell.text

            counter += 1
        list_of_teams.append([team_information])

    return list_of_teams

def download_musics_in_channel(channel_name:str, limit:int=0):
    '''
    channel_name : is the channel most be download music form it.
    limit : is an number for set limit of download music from channel.
    '''
    api_id = '7307076'
    api_hash = '587515b54cebf370f9cc17f478470aed'
    bot_token = '1972157339:AAFqAgiV2zi1evZlMJG4TxW5KffO28-fYak'
    
    bot = TelegramClient('music', api_id, api_hash)

    with bot:

        if limit == 0 :
            musics = bot.get_messages(channel_name, filter=InputMessagesFilterMusic)
        elif isinstance(limit,int):
            musics = bot.get_messages(channel_name,limit, filter=InputMessagesFilterMusic)

        for m in musics:
            bot.download_media(m)

def get_course_episode_link_from_maktabkhoneh(mail,password,course_url):
    '''
    mail : the mail you signup in maktabkhoneh
    password : your maktabkhoneh account password
    course_url : the url of course should extract episode link 
    '''
    base_url = 'https://maktabkhooneh.org'

    option = webdriver.ChromeOptions()
    #option.headless = True
    driver = webdriver.Chrome(options=option)

    #region login
    b_xpath = '/html/body/div[1]/nav/div/div[2]/div[3]/button'
    e_i_xpath = '/html/body/div[1]/div[5]/div/div[1]/div[2]/div/form/div/input'
    e_l_xpath = '/html/body/div[1]/div[5]/div/div[1]/div[2]/div/form/input[3]'
    p_i_xpath = '/html/body/div[1]/div[5]/div/div[1]/div[2]/div/div[1]/form/div/input[2]'
    p_l_xpath = '/html/body/div[1]/div[5]/div/div[1]/div[2]/div/div[1]/form/input[2]'
    do_not_show_me_xpath = '//*[@id="page_message__text"]/div/div/button[2]'
    
    driver.get(base_url)
    driver.find_element(By.XPATH, b_xpath).click()
    sleep(1)
    
    driver.find_element(By.XPATH, e_i_xpath).send_keys(mail)
    driver.find_element(By.XPATH, e_l_xpath).click()
    sleep(3)
    
    driver.find_element(By.XPATH, p_i_xpath).send_keys(password)
    sleep(0.5)
    
    driver.find_element(By.XPATH, p_l_xpath).click()
    sleep(8)
    driver.find_element(By.XPATH,do_not_show_me_xpath).click()
    #endregion login

    driver.get(course_url)

    bs = bs4.BeautifulSoup(driver.page_source)

    counter = 0
    for a in bs.findAll('a', attrs='chapter__unit'):
        if counter < 1 :
            if 'کوییز' not in a.attrs['title'] and 'پروژه' not in a.attrs['title']:
                a_href = a.attrs['href']
                driver.get(base_url + a_href)
                bs2 = bs4.BeautifulSoup(driver.page_source)
            
                source = bs2.find('source', attrs='js-player__source')
                video_source = source['src']
                with open('links.txt', 'a') as handle:
                    handle.write(video_source + '\n\n')
        counter + 1
   