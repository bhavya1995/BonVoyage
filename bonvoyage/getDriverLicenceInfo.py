from selenium import webdriver
from bs4 import BeautifulSoup
import time

webpage = r"https://dlpay.dimts.in/dldetail/default.aspx"
searchterm = "DL-1120140273904"
driver = webdriver.Chrome()
driver.get(webpage)
sbox = driver.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_txtdlno")
sbox.send_keys(searchterm)
submit = driver.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_Button1")
submit.click()
time.sleep(10)
page = driver.page_source
# print(page)
soup = BeautifulSoup(page)
# print(soup)
counter = 1

for s in soup.select('input'):
	if (counter == 5 or counter == 9 or counter == 10 or counter == 11 or counter == 12 or counter == 15 or counter == 14):
		print(s.get('value'))
	counter += 1