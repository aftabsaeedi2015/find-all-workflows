from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# # Initialize the Selenium web driver
# service = Service('./chromedriver')
# chrome_options = Options()
# chrome_options.add_argument('--headless')
# create a new instance of the Chrome driver
# driver = webdriver.Chrome(options=chrome_options)
driver = webdriver.Chrome('./chromedriver')

driver.get('https://webdriveruniversity.com')
