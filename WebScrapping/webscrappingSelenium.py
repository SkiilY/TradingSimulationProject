from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import re
import pandas as pd
import datetime
from time import sleep
import os

def xpath_element(xpath):
    try:
        element = driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        element = []
    return element

def real_time_price(stock_code):
    url = 'https://finance.yahoo.com/quote/' + stock_code + '?p=' + stock_code + '&.tsrc=fin-srch'
    sleep(1)
    driver.get(url)
    
    ###############################################
    
    xpath = '//*[@id="quote-header-info"]/div[3]/div[1]/div'
    stock_price_info = xpath_element(xpath)
    
    if stock_price_info != []:
        stock_price_temp = stock_price_info.text.split()[0]
        if stock_price_temp.find('+')!=-1:
            price = stock_price_temp.split('+')[0]
            try:
                change = '+' + stock_price_temp.split('+')[1] + ' ' + stock_price_info.text.split()[1]
            except IndexError:
                change = []
        elif stock_price_temp.find('-')!=-1:
            price = stock_price_temp.split('-')[0]
            try:
                change = '-' + stock_price_temp.split('-')[1] + ' ' + stock_price_info.text.split()[1]
            except IndexError:
                change = []
        else:
            price, change = [], []
    else:
        price, change = [], []
        
    ###############################################
    
    xpath = '//*[@id="quote-summary"]/div[1]'
    volume_temp = xpath_element(xpath)
    if volume_temp != []:
        for i, text in enumerate(volume_temp.text.split()):
            if text == 'Volume':
                volume = volume_temp.text.split()[i+1]
                break
            else:
                volume = []
    else:
        volume = []
        
    ###############################################
    
    xpath = '//*[@id="quote-summary"]/div[2]'
    target_temp = xpath_element(xpath)
    if target_temp != []:
        for i, text in enumerate(target_temp.text.split()):
            if text == 'Est':
                if target_temp.text.split()[i+1] != 'N/A':
                    one_year_target = target_temp.text.split()[i+1]
                else:
                    one_year_target = []
                break
            else:
                one_year_target = []
    else:
        one_year_target = []
        
    ###############################################
    
    latest_pattern = []
    
    ###############################################

    return [price, change, volume, latest_pattern, one_year_target]

chrome_options = Options()
chrome_options.add_argument('--headless')# not show window
chrome_options.add_argument("--log-level=3")
log_path=os.devnull
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(options=chrome_options)
url = 'https://fr.finance.yahoo.com/quote/'
    
driver.get(url)
sleep(2)
accepter_button = driver.find_element(By.XPATH, '//*[@id="consent-page"]/div/div/div/form/div[2]/div[2]/button[1]')
if accepter_button:
    accepter_button.click()

Stock=['META']
while (True):
    info = []
    # shift to US time 13 hours winter, 12 hours summer
    time_stamp = datetime.datetime.now() - datetime.timedelta(hours=6)
    time_stamp = time_stamp.strftime("%Y-%m-%d %H:%M:%S")

    for stock_code in Stock:
        stock_price, change, volume, latest_pattern, one_year_target = real_time_price(stock_code)
        info.append(stock_price)
        info.extend([change])
        info.extend([volume])
        if latest_pattern != []:
            info.extend([latest_pattern])
        info.extend([one_year_target])

    col = [time_stamp]
    col.extend(info)
    columns = ['time', 'stock_price', 'change', 'volume', 'one_year_target']
    df = pd.DataFrame([col], columns=columns)
    df.to_csv(str(time_stamp[0:11]) + 'stock data.csv', mode='a', header=False, index=False)

driver.quit()