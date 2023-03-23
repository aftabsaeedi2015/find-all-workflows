import requests
from bs4 import BeautifulSoup
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from urllib.parse import urlparse
from selenium.webdriver.chrome.options import Options

# from screenshot import get_screenshot



# Initialize the Selenium web driver
service = Service('./chromedriver')
chrome_options = Options()
chrome_options.add_argument('--headless')
# create a new instance of the Chrome driver
driver = webdriver.Chrome(options=chrome_options)
driver = webdriver.Chrome(service=service)
count=1
b_url = 'https://app.usemango.co.uk'
flag = 0
def crawl(url, visited_links, current_workflow,count,flag):
    print(flag)
    if url in visited_links:
        print("exists already")
        print("before : ",flag)
        flag=flag+1
        print("after : ",flag)

        # if(flag==2):
        #     get_screenshot(current_workflow)
        f = open("demo2.json", "a")
        f.write(json.dumps(current_workflow))
        f.write("\n")
        f.close()

        # get screenshots

        # Remove the current link from the current workflow and return
        if(len(current_workflow)!=0):
            k = current_workflow.pop()
            print('pop'+'   '+k)
        return flag

    # Add the URL to the set of visited links
    visited_links.add(url)

    # Add the default protocol if none is supplied


    # Send an HTTP request to the URL and retrieve the response
    # print(url)
    print("url"+url)
    response = requests.get(url)

    # Retrieve the session ID from the response headers
    # Print the session ID
    # session_id = response.cookies.get('session_id')
    # print("Session ID:", session_id)
    # print(url)

    # Parse the HTML content of the response using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all links on the page
    links = soup.find_all('a',href=True)
    print(soup)



    # If there are no new links
    if not links:
        print("inside no link found")
        f = open("demo2.json", "a")
        f.write(json.dumps(current_workflow))
        f.write("\n")
        f.close()
        flag=flag+1
        # if(flag==2):
        #     get_screenshot(current_workflow)


        if(len(current_workflow)!=0):
            k = current_workflow.pop()
            print('pop'+'   '+k)
        return flag

    # Loop through new links and add them to the current workflow and visited links
    else:
        for link in links:
            print(links)
            new_url = link.get('href')
            if not new_url.startswith('http'):
                if not new_url.startswith('/'):
                    new_url='/'+new_url
                new_url = b_url+new_url
            # check if internal link
            if new_url is not None and new_url.startswith(b_url):
                current_workflow.append(new_url)

                # get a screenshot when a new url is added to the current workflow
                # driver.get(new_url)
                # filename = str(count) + '.png'
                # driver.save_screenshot(filename)
                # count+=1
                # driver.implicitly_wait(1)
                # Recursively crawl the new link
                print("before recursive call :",flag)
                flag=crawl(new_url, visited_links, current_workflow,count,flag)

    # remove the parent after all its children are looped through
    if(len(current_workflow)!=0):
        current_workflow.pop()

    return flag


# Example usage
visited_links = set()
current_workflow = ['https://app.usemango.co.uk']



crawl(b_url, visited_links, current_workflow,count,flag)

