from selenium import webdriver
from colorama import Fore, Back, Style
from dotenv import dotenv_values
from selenium.webdriver.chrome.options import Options
from decimal import *
import time
import datetime
import sys
import os

chrome_options = Options()
chrome_options.add_argument("--headless")
config = dotenv_values(".env")
URL = str(sys.argv[1]) if (len(sys.argv) == 2) else config["URL"]
driver = webdriver.Chrome(options=chrome_options)
driver.get(URL)
driver.implicitly_wait(10)
hour_bal_time = 0
prev_bal = 0
cur_bal = 0
hour_bal_gain = 0.0
has_twelve_calculated = False
has_twentyfour_calculated = False
twelve_hour_counter = 0
twelve_hour_time = 0
twentyfour_hour_counter = 0
twentyfour_hour_timer = 0
twentyfour_hour_time = 0
setup = True
time.sleep(3)
while True:
    unpaid = driver.find_element_by_xpath(
        '//*[@id="app"]/main/div/div[2]/div[1]/div[2]/div[2]/div[2]/div/span[1]').text
    average = driver.find_element_by_xpath(
        '//*[@id="app"]/main/div/div[2]/div[1]/div[3]/div[1]/div/div[2]/div/div[2]/span[1]').text
    curr = driver.find_element_by_xpath(
        '//*[@id="app"]/main/div/div[2]/div[1]/div[3]/div[1]/div/div[1]/div/div[2]/span[1]').text
    reported = driver.find_element_by_xpath(
        '//*[@id="app"]/main/div/div[2]/div[1]/div[3]/div[1]/div/div[3]/div/div[2]/span[1]').text
    valid = driver.find_element_by_xpath(
        '//*[@id="app"]/main/div/div[2]/div[1]/div[3]/div[2]/div/div[1]/div/div[2]/span').text
    stale = driver.find_element_by_xpath(
        '//*[@id="app"]/main/div/div[2]/div[1]/div[3]/div[2]/div/div[2]/div/div[2]/span').text
    rejected = driver.find_element_by_xpath(
        '//*[@id="app"]/main/div/div[2]/div[1]/div[3]/div[2]/div/div[3]/div/div[2]/span').text
    cur_bal = Decimal(unpaid)
    x = datetime.datetime.now()
    if setup:
        prev_bal = Decimal(unpaid)
        hour_bal_time = x.hour
        setup = False
    if (hour_bal_time != x.hour):
        hour_bal_time = x.hour
        twentyfour_hour_timer += 1
        if (cur_bal > prev_bal):
            hour_bal_gain = cur_bal - prev_bal
            prev_bal = cur_bal
            twelve_hour_counter += hour_bal_gain
            twentyfour_hour_counter += hour_bal_gain
        else:
            hour_bal_gain = 0.0

    if twentyfour_hour_timer == 12 or twentyfour_hour_timer == 24:
        twelve_hour_counter = twelve_hour_counter / 12
        twentyfour_hour_time = x
        has_twelve_calculated = True
    if twentyfour_hour_timer == 24:
        twentyfour_hour_counter = twentyfour_hour_counter / 24
        has_twentyfour_calculated = True

    print(Fore.WHITE + "Unpaid: " + Fore.YELLOW + "{}".format(unpaid) + Fore.WHITE + " ETH" + Fore.CYAN + " @{}".format(x) +
          Fore.WHITE + " |" + Fore.MAGENTA + " AVG@{}MH/S".format(average) + Fore.WHITE + " ; " + Fore.MAGENTA + "CUR@{}MH/S".format(curr) + Fore.WHITE + " ; " + Fore.MAGENTA + "REP@{}MH/S".format(reported) + Fore.WHITE + " |")
    print(Fore.GREEN + "Valid: {}".format(valid) + Fore.WHITE + " ; " + Fore.YELLOW +
          "Stale: {}".format(stale) + Fore.WHITE + " ; " + Fore.RED + "Rejected: {}".format(rejected))
    print(Fore.WHITE + "Hourly Gain: " + Fore.GREEN + " {}".format(hour_bal_gain) +
          Fore.WHITE + " ETH; Last Updated" + Fore.CYAN + " @{}:00hrs".format(hour_bal_time))
    if has_twelve_calculated:
        print(Fore.WHITE + "Last 12HR Gain: " + Fore.GREEN + " {}".format(twelve_hour_counter) +
            Fore.WHITE + " ETH; Last Updated" + Fore.CYAN + " @{}".format(twelve_hour_time))
    else:
        print(Fore.WHITE + "Last 12HR Gain: " + Fore.YELLOW + " Not Calculated until {} more hours".format(12-twelve_hour_counter) +
            Fore.WHITE + " ; Last Updated" + Fore.CYAN + " @{}".format(x))

    if has_twentyfour_calculated:
            print(Fore.WHITE + "Last 12HR Gain: " + Fore.GREEN + " {}".format(twentyfour_hour_counter) +
                Fore.WHITE + " ETH; Last Updated" + Fore.CYAN + " @{}".format(twentyfour_hour_time))
    else:
        print(Fore.WHITE + "Last 24HR Gain: " + Fore.YELLOW + " Not Calculated until {} more hours".format(24-twentyfour_hour_counter) +
            Fore.WHITE + " ; Last Updated" + Fore.CYAN + " @{}".format(x))

    if twentyfour_hour_timer == 24 or twentyfour_hour_timer == 12:
        twentyfour_hour_counter = 0
        twentyfour_hour_timer = 0
        twelve_hour_counter = 0


    driver.refresh()
    time.sleep(30)
