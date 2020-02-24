from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException
import argparse
import random
from XPATHS import *

SLEEP_SECONDS = 2
RANDOM_PERCENTAGE = 0.3

URL = "https://www.linkedin.com"
KEYWORD_SEARCH_URL = "https://www.linkedin.com/search/results/people/?keywords="


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
	profile_links = set(driver.find_elements(By.XPATH, XPATH_PROFILE_URL))
	
	for profile_link in {link.get_attribute("href") for link in profile_links}:
		if should_proceed():
			print(f'View: {profile_link}')
			driver.get(profile_link)
			wait()


#Find all connect buttons and click them and confirm Send Now
def send_connection_invites(driver):
	connect_buttons = driver.find_elements(By.XPATH, XPATH_SEARCH_CONNECT_BUTTON)

	for connect in connect_buttons:
		if should_proceed():
			try:
				connect.click()
				driver.find_element(By.XPATH, XPATH_SEARCH_CONNECT_CONFIRM).click()
				print('Connection Invite Sent')
				wait()
			except ElementClickInterceptedException:
				#Linkedin may ask for the name of the person
				#you're sending invite or you receive a message
				#and we will just skill that for now
				print("Error: Could not send invite.")


#Loads keyword search
def keyword_search(driver, keyword, pages, mode):
	driver.get(f'{KEYWORD_SEARCH_URL}{keyword}')

	for page in range(2, pages + 1):
		#Takes different actions based on MODE
		if mode == 1:
			send_connection_invites(driver)
		elif mode == 2:
			profile_viewer(driver)
		else: break

		driver.get(f'{KEYWORD_SEARCH_URL}{keyword}&page={page}')


def main(email, password, keyword, pages, mode):
	driver = webdriver.Firefox(executable_path='geckodriver.exe')

	start_login(driver, email, password, keyword)
	keyword_search(driver, keyword, pages, mode)

	driver.close()

if __name__=="__main__":
	argparser = argparse.ArgumentParser()
	argparser.add_argument('email', help = 'Login Email')
	argparser.add_argument('password', help = 'Login Password')
	argparser.add_argument('keyword', help = 'Search Keyword')
	argparser.add_argument('pages', help = 'How many pages to search', type=int)
	argparser.add_argument('mode', help = 'What mode to run the script on', type=int)

	args = argparser.parse_args()
	email = args.email
	password = args.password
	keyword = args.keyword
	pages = args.pages
	mode = args.mode
	
	main(email, password, keyword, pages, mode)