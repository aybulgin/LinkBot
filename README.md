# LinkedIn Bot
Simple simple that allows you to grow your linkedin network by sending connection invites or profile views.

## Installation
To run this script you need three main components:
- Python 3 (python.org)
- Mozilla Firefox Browser (firefox.com)
- Firefox Selenium Driver (https://github.com/mozilla/geckodriver/releases)

If you have these installed and the firefox driver (geckodriver.exe) in PATH, run `pip install -r requirements.txt` inside the app folder in the console.

## Before starting
After the installation you need to update the some variables in `credentials.py` and `settings.py` files with your own. 
  
### Credentials.py
- Email (Your linkedin login)
- Password (Your linkedin password)
### Settings.py
- SEARCH_KEYWORK (What keyword related profiles you want to search. Ex: founder)
- ACTION_LIMIT (How many connections/views you want to send)
- MODE
  1. 1: Send invites to profiles based on people keyword search  
  2. 2: Profile viewer based on on people keyword search  
- HEADLESS (True if you don't want to see and browser and false if you do)
- SLEEP_SECONDS (How much time to wait between actions)
- RANDOM_PERCENTAGE (Before executing an action the script will evaluate a random number and compare to this variable. ex: 0.3 means the script will send a connection invite or a view one third of the time)

## Running the script
After installing the requirments and updating the settings and credentials you can run the script with the following command in the console
- ```python app.py```

## Changelog
- 0.2.4 - Move start arguments to variables in settings and credentials' files and implement action limits
- 0.2.3 - Optional headless browser support
- 0.2.2 - Added stop mechanism to close script when connect rate limited
- 0.2.1 - Error handling on connection invites and randomize main actions
- 0.2 - Added a profile viewer and Mode argument to switch between functions
- 0.1 - Simple script to send connection invites 

## Disclaimer
USE AT YOUR OWN RISK.