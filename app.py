from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.firefox.options import Options
import argparse
import random
from XPATHS import *
from settings import *
from credentials import *


def wait():
	sleep(SLEEP_SECONDS)


#Randomize actions based on predefined percentage
def should_proceed():
	if random.random() < RANDOM_PERCENTAGE: return True
	else: return False


def start_login(driver, email, password, keyword):
	try: driver.get(URL + "/login")
	except TimeoutException: start_login(driver, email, password, keyword)

	driver.find_element(By.XPATH, XPATH_LOGIN_EMAIL).send_keys(email)
	wait()
	driver.find_element(By.XPATH, XPATH_LOGIN_PASSWORD).send_keys(password)
	wait()
	driver.find_element(By.XPATH, XPATH_LOGIN_SUBMIT).click()

	if "add-phone" in driver.current_url:
		driver.find_element(By.XPATH, XPATH_SKIP_ADD_PHONE).click()


#Scrape profile links in current page and visits them
def profile_viewer(driver):
	global ACTION_COUNTER
	profile_links = set(driver.find_elements(By.XPATH, XPATH_PROFILE_URL))
	
	for profile_link in {link.get_attribute("href") for link in profile_links}:
		if should_proceed():
			driver.get(profile_link)
			print(f'[OK] View sent {profile_link}')
			ACTION_COUNTER += 1
			wait()


#Find all connect buttons and click them and confirm Send Now
def send_connection_invites(driver):
	global KILLSWITCH
	global ACTION_COUNTER
	connect_buttons = driver.find_elements(By.XPATH, XPATH_SEARCH_CONNECT_BUTTON)

	for connect in connect_buttons:
		if should_proceed():
			try:
				connect.click()
				#If you run out of invites we should stop the keyword search loop
				try:
					if driver.find_element(By.XPATH, XPATH_CONNECT_LIMIT):
						KILLSWITCH = True
				except: pass
				driver.find_element(By.XPATH, XPATH_SEARCH_CONNECT_CONFIRM).click()
				print('[OK] Connection Invite Sent')
				ACTION_COUNTER += 1
				wait()
			except ElementClickInterceptedException:
				#Linkedin may ask for the name of the person
				#you're sending invite or you receive a message
				print("[Error] Could not send invite.")


#Loads keyword search
def keyword_search(driver, keyword, pages, mode):
	driver.get(f'{KEYWORD_SEARCH_URL}{keyword}')
	page = 1 #start counting

	#We're going to limit the actions based on our limit
	while (ACTION_COUNTER <= ACTION_LIMIT):
		#If we run out of invites or get limited we should stop
		if KILLSWITCH:
			print('[INFO] Connection Invite Rate Limit Active.')
			break
		#Takes different actions based on MODE
		if mode == 1:
			send_connection_invites(driver)
		elif mode == 2:
			profile_viewer(driver)
		else: break

		page += 1 #increment page before moving on
		driver.get(f'{KEYWORD_SEARCH_URL}{keyword}&page={page}')


def main(email, password, keyword, pages, mode):
	#Run browser headless without visible UI
	if HEADLESS:
		options = Options()
		options.headless = True
		driver = webdriver.Firefox(executable_path='geckodriver.exe', options=options)
	else: driver = webdriver.Firefox(executable_path='geckodriver.exe')
	print('[OK] Browser Started')

	start_login(driver, email, password, keyword)
	keyword_search(driver, keyword, pages, mode)
	print('[DONE]')
	driver.close()


if __name__=="__main__":
	#Get variables from credentials.py and settings.py files
	email = LOGIN_EMAIL
	password = LOGIN_PASSWORD
	keyword = SEARCH_KEYWORD
	pages = ACTION_LIMIT
	mode = MODE
	
	main(email, password, keyword, pages, mode)