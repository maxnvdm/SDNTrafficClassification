from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import time
import subprocess

#/mnt/vol1/vulatest/pcap
#/home/max/
#tcpdump = 'sudo timeout 930 tcpdump -i d1-eth0 -w /mnt/vol1/d1outlooktrainhome1.pcap'
#process = subprocess.Popen(tcpdump.split())
opts = Options()

# Turn to false to open friefox
opts.headless = True

browser = Firefox(options=opts)
browser.get('https://outlook.com/myuct.ac.za')
time.sleep(5)
email_input = browser.find_element_by_id('userNameInput')
email_input.send_keys('vmrmax002@myuct.ac.za')

pass_input = browser.find_element_by_id('passwordInput')
pass_input.send_keys('password')
pass_input.submit()
time.sleep(5)
browser.find_element_by_id('idSIButton9').click()
delay = 15

try:
    myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'html[dir] ._1xP-XmXM1GGHpRKCCeOKjP')))
    print("Page is ready")
except TimeoutException:
    print("Loading took too much time")
inbox_email = browser.find_elements_by_class_name('_1xP-XmXM1GGHpRKCCeOKjP')
inbox_email[1].click()

for email in range(15):
    time.sleep(20)
    print("Next email")
    inbox_email[1].send_keys(Keys.ARROW_DOWN)

browser.quit()
