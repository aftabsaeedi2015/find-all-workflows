from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Initialize the Selenium web driver
service = Service('./chromedriver')
chrome_options = Options()
chrome_options.add_argument('--headless')
# create a new instance of the Chrome driver
driver = webdriver.Chrome(options=chrome_options)
driver = webdriver.Chrome(service=service)


def get_screenshot(num):
    count=1
    file1 = open('demo.json', 'r')
    workflows = file1.readlines()
    # Strips the newline character
    for workflow in workflows:
        if(count==num):
            for url in eval(workflow):
                print(url)
                driver.get(url)
                filename = str(count) + '.png'
                driver.save_screenshot(filename)
                count+=1
            driver.quit()
        count+=1
get_screenshot(33)
