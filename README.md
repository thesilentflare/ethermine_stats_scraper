![Alt text](/screenshots/etherminestats.png?raw=true)

# Ethermine Stats Scraper

Simple python script that outputs ethermine dashboard stats and more.
**NOTE:** Hourly gain may take at least 2hrs to be near accurate to the data taken from ethermine dashboard.

# Screenshots

![SS 1](/screenshots/console_example.png?raw=true)
![SS 2](/screenshots/console_example2.png?raw=true)

# Dependencies

- python 3.8+
- google chrome v88+
- chromedriver v88+
- pip
  - selenium
  - colorama
- valid ethermine dashboard URL

# Configuration

Run `setup.sh` to install any required python packages.
Chrome and chromedriver must be installed (chromedriver must be added to `PATH`).
Add your ethermine url to the `config.ini` file or include it as the first argument when calling `crawl.py`.

# Features

Condensed stats that show the following:

- Unpaid ETH balance
- hashrates (average, current, reported) [^1]
- shares (valid, stale, rejected)
- hourly ETH gain [^2]
- 12hr ETH gain (since started logging) [^2]
- 24hr ETH gain (since started logging) [^2]

[^2]: Gains are calculated based on scraped values from ethermine dashboard and are only meant to be an estimate. Will not account for the hour where Ethermine pays the Unpaid balance.

[^1]: All hashrates are in MH/S.
