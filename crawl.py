from selenium import webdriver
from colorama import Fore, Back, Style
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from decimal import *
import configparser
import time
import datetime
import sys
import signal

### SIGINT Handler ###
def signal_handler(sig, frame):
    x = datetime.datetime.now()
    print(Style.BRIGHT + Fore.RED + 'Keyboard Interrupt detected at @{}'.format(x))
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)
#############################################

### Convert DateTime for UPTIME Functions ###
def date_diff_in_seconds(dt2, dt1):
    timedelta = dt2 - dt1
    return timedelta.days * 24 * 3600 + timedelta.seconds

def dhms_from_seconds(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    return (days, hours, minutes, seconds)
#############################################


# Configs
conf = configparser.ConfigParser()
conf.read('config.ini')
chrome_options = Options()
chrome_options.add_argument("--headless")
URL = str(sys.argv[1]) if (len(sys.argv) == 2) else conf["etherminer"]["URL"]
driver = webdriver.Chrome(options=chrome_options)
REFRESH = conf["refresh"]["TIME"]

# Test URL
try:
    driver.get(URL)
except:
    print("URL INVALID")
    driver.quit()
    sys.exit(0)
#driver.implicitly_wait(10)
delay = 15
try:
    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/main/div/div[2]/div[1]/div[3]/div[1]/div/div[3]/div/div[2]/span[1]')))
    print("Page is ready!")
except TimeoutException:
    print("Loading took too much time!")
    driver.quit()
    sys.exit(0)

# Initial Variables
started_time = 0
uptime = 0
hour_bal_time = 0
prev_bal = 0
cur_bal = 0
hour_bal_gain = 0.00000
has_twelve_calculated = False
has_twentyfour_calculated = False
twelve_hour_counter = Decimal(0)
twelve_hour_time = 0
twentyfour_hour_counter = Decimal(0)
twentyfour_hour_timer = 0
twentyfour_hour_time = 0
twentyfour_hour_low = 0
twentyfour_hour_high = 0
est_gain = Decimal(0)
setup = True
#time.sleep(3)

# Main Loop
while True:
    # Scrape dashboard for data
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

    # Logic
    if setup:
        prev_bal = Decimal(unpaid)
        hour_bal_time = x.hour
        started_time = x
        twentyfour_hour_low = curr
        twentyfour_hour_high = curr
        setup = False
    # Uptime counter
    uptime = dhms_from_seconds(date_diff_in_seconds(x, started_time))
    if curr < twentyfour_hour_low:
        twentyfour_hour_low = curr
    elif curr > twentyfour_hour_high:
        twentyfour_hour_high = curr
    # per hr counter
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
        est_gain += hour_bal_gain + (24 - twentyfour_hour_timer) * hour_bal_gain
    # 12hr counter
    if twentyfour_hour_timer == 12 or twentyfour_hour_timer == 24:
        #twelve_hour_counter = twelve_hour_counter / 12
        twelve_hour_time = x
        has_twelve_calculated = True
    # 24hr counter
    if twentyfour_hour_timer == 24:
        #twentyfour_hour_counter = twentyfour_hour_counter / 24
        twentyfour_hour_time = x
        has_twentyfour_calculated = True

    ### DISPLAY BLOCK ###
    print(Back.WHITE + Fore.BLACK + "Time Started Logging: {} | ".format(started_time) +
          "UPTIME: {0[0]}days {0[1]}hrs {0[2]}mins {0[3]}s".format(uptime) + Back.RESET)
    print(Fore.WHITE + "Unpaid: " + Fore.YELLOW + "{}".format(unpaid) + Fore.WHITE + " ETH" + Fore.CYAN + " @{}".format(x) +
          Fore.WHITE + " |" + Fore.MAGENTA + " AVG@{}MH/S".format(average) + Fore.WHITE + " ; " + Fore.MAGENTA + "CUR@{}MH/S".format(curr) + Fore.WHITE + " ; " + Fore.MAGENTA + "REP@{}MH/S".format(reported) + Fore.WHITE + " |")
    print(Fore.GREEN + "Valid: {}".format(valid) + Fore.WHITE + " ; " + Fore.YELLOW +
          "Stale: {}".format(stale) + Fore.WHITE + " ; " + Fore.RED + "Rejected: {}".format(rejected))
    print(Fore.WHITE + "Hourly Gain: " + Fore.GREEN + " {:.5f}".format(hour_bal_gain) +
          Fore.WHITE + " ETH | Est. Daily Gain: " + Fore.GREEN + "{:.5f}".format(est_gain) + Fore.WHITE + " ETH ; Last Updated" + Fore.CYAN + " @{}:00hrs".format(hour_bal_time))
    if has_twelve_calculated:
        print(Fore.WHITE + "Last 12HR Gain: " + Fore.GREEN + " {}".format(twelve_hour_counter) +
              Fore.WHITE + " ETH; Last Updated" + Fore.CYAN + " @{}".format(twelve_hour_time))
    else:
        print(Fore.WHITE + "Last 12HR Gain: " + Fore.YELLOW + " Not Calculated until {} more hours".format(12-twentyfour_hour_timer) +
              Fore.WHITE + " ; Last Updated" + Fore.CYAN + " @{}".format(x))

    if has_twentyfour_calculated:
        print(Fore.WHITE + "Last 12HR Gain: " + Fore.GREEN + " {}".format(twentyfour_hour_counter) +
              Fore.WHITE + " ETH; Last Updated" + Fore.CYAN + " @{}".format(twentyfour_hour_time))
    else:
        print(Fore.WHITE + "Last 24HR Gain: " + Fore.YELLOW + " Not Calculated until {} more hours".format(24-twentyfour_hour_timer) +
              Fore.WHITE + " ; Last Updated" + Fore.CYAN + " @{}".format(x))
    print(Fore.WHITE + "24HRS LO/HI POOL Hashrates: " + Fore.MAGENTA + " LOW@{}MH/S".format(twentyfour_hour_low) + Fore.WHITE + " ; " + Fore.MAGENTA + "HIGH@{}MH/S".format(twentyfour_hour_high) + Fore.WHITE + " | ")

    print(Fore.WHITE + "-----------------------------------------------------------------------------------------------")
    ### END OF DISPLAY BLOCK ###

    # Reset counters as needed
    if twentyfour_hour_timer == 24 or twentyfour_hour_timer == 12:
        twentyfour_hour_counter = 0
        twentyfour_hour_timer = 0
        twelve_hour_counter = 0
        twentyfour_hour_high = curr
        twentyfour_hour_low = curr
        est_gain = 0

    # Refresh page and sleep
    time.sleep(int(REFRESH) - 3)
    driver.refresh()
    time.sleep(3)
