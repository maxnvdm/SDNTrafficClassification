from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import time
import subprocess

#/mnt/vol1/vulatest/pcap
#/home/max/
#tcpdump = 'sudo timeout 930 tcpdump -i d1-eth0 -w /mnt/vol1/d1vulatrainhome1.pcap'
#process = subprocess.Popen(tcpdump.split())

opts = Options()

# Turn to false to open friefox
opts.headless = True

browser = Firefox(options=opts)
browser.get('https://vula.uct.ac.za/portal/login')
time.sleep(6)
#print(browser.page_source)
username_input = browser.find_element_by_name('UserName')
username_input.send_keys('vmrmax002@wf.uct.ac.za')
pass_input = browser.find_element_by_id('passwordInput')
pass_input.send_keys('password')
pass_input.submit()
time.sleep(5)
browser.get('https://vula.uct.ac.za/portal/site/32fda59f-771c-45d2-ad2a-7a6978b65868')
time.sleep(5)
#videos = browser.find_element_by_xpath("//a[@title='Lecture Videos']")
browser.get('https://vula.uct.ac.za/portal/site/32fda59f-771c-45d2-ad2a-7a6978b65868/page/d70ceb86-f668-4ef6-861c-7211a8107730')
time.sleep(5)
#browser.switch_to_frame("LtiLaunchFrame_8108fc5b_5981_4561_bf41_b5f99a51fdec")
#browser.find_element_by_xpath("//a[@href='/engage/theodul/ui/core.html?ltimode=true&id=84a94ab4-fff9-480b-8492-1da1a4ec8a57']").click()
browser.get('https://media.uct.ac.za/engage/theodul/ui/core.html?ltimode=true&id=84a94ab4-fff9-480b-8492-1da1a4ec8a57')
time.sleep(5)
#print(browser.page_source)
action = ActionChains(browser)
action.send_keys(Keys.SPACE)
action.perform()


# TODO set timer to end driver
time.sleep(880)
browser.quit()
