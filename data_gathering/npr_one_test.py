import selenium
import time
from selenium.webdriver.firefox.options import Options as options
from selenium.webdriver.firefox.service import Service

#///////////////// Init binary & driver
new_driver_path = r'C:\Users\kyvin\SeleniumDrivers\geckodriver.exe'
new_binary_path = r'C:\Program Files\Mozilla Firefox\firefox.exe'

ops = options()
ops.binary_location = new_binary_path
serv = Service(new_driver_path)
driver = selenium.webdriver.Firefox(service=serv, options=ops)

driver.get('https://www.npr.org/programs/all-things-considered/archive?date=12-31-2021')
SCROLL_PAUSE_TIME = 10

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

time.sleep(10)
driver.quit()