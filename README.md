# LinkedIn Bot

## Installation
To run this script you need three main components:
- Python 3 (python.org)
- Mozilla Firefox Browser (firefox.com)
- Firefox Selenium Driver (https://github.com/mozilla/geckodriver/releases)

If you have these installed and the firefox driver (geckodriver.exe) in PATH, run `pip install -r requirements.txt` inside the app folder in the console.

## Running the script
After the installation you can run the script with the following command in the console
- ```python app.py <your@email.com> <password> <keyword> <pages> <mode>```
### Arguments
- Email (Your linkedin login)
- Password (Your linkedin password)
- Keyword (What keyword related profiles you want to search. Ex: founder)
- Pages (How many pages do you want to look for new connections)
- Mode
   MODE 1: Send invites to profiles based on people keyword search  
   MODE 2: Profile viewer based on on people keyword search  

The script will open Firefox and look for people related to your keyword then send them a connection invite.

## Changelog
- 0.2 - Added a profile viewer and Mode argument to switch between functions
- 0.1 - Simple script to send connection invites 

## Disclaimer
USE AT YOUR OWN RISK.