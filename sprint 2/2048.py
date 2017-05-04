#! python3
# 2048.py - Plays the 2048 game by itself


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

browser = webdriver.Firefox()
browser.get('https://gabrielecirulli.github.io/2048/')

htmlElem = browser.find_element_by_tag_name('html') # 'selects' the whole page to make sure the keys get sent to the game interface
time.sleep(3) # waits for the page to load

while True: # plays the game indefinetively
    htmlElem.send_keys(Keys.RIGHT)
    htmlElem.send_keys(Keys.DOWN)
    htmlElem.send_keys(Keys.LEFT)
    htmlElem.send_keys(Keys.UP)

