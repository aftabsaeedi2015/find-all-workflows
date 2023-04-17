import requests
from bs4 import BeautifulSoup
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from urllib.parse import urlparse
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from assign_tag import assign_tag
from assign_tag import check_tag_exists
from assign_tag import convert_url_to_tags
from valid_url import check_url
import uuid
from lxml import etree
import re

# from screenshot import get_screenshot



# Initialize the Selenium web driver
# service = Service('./chromedriver')
# chrome_options = Options()
# chrome_options.add_argument('--headless')
# # create a new instance of the Chrome driver
# driver = webdriver.Chrome(options=chrome_options)
# driver = webdriver.Chrome(service=service)

b_url = 'https://demo-website-drab-three.vercel.app'



def generate_unique_id():
    return str(uuid.uuid4())

def crawl(url, visited_links, current_workflow,parent_id,tag,e_id,e_class,e_xpath):
    parent = {
        'id': generate_unique_id(),
        'url': url,
        'locators':[{'id':e_id,'class':e_class,'xpath':e_xpath}],
        'tag':tag,
        'parent_id':parent_id,
        'children': []
    }
    if url in current_workflow and  current_workflow.count(url)>1:
        # current_workflow.append(url)
        # Remove the current link from the current workflow and return
        if(len(current_workflow)!=0):
            # if it is a login workflow store it
            f = open("all_workflows.txt", "a")
            f.write(str(current_workflow))
            f.write("\n")
            f.close()
            current_workflow.pop()
        # visited_links.pop()
        return parent

    # Add the URL to the set of visited links
    else:
        visited_links.add(url)
    # Send an HTTP request to the URL and retrieve the response
    # print(url)

        response = requests.get(url)

        # Parse the HTML content of the response using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        # driver.get(b_url)
        # links = driver.find_elements(By.TAG_NAME, 'a')
        body = soup.body
        style_tag = soup.find('style')
        if style_tag is not None:
            style_tag.extract()
        for script in soup.find_all("script"):
            script.extract()
        soup = soup.prettify()

        lxml_tree = etree.fromstring(str(soup).strip())
        a_tags = lxml_tree.findall('.//a')
        if not a_tags:
            if(len(current_workflow)!=0):
                for key in filtered_workflow.keys():
                    if(check_tag_exists(current_workflow,key)):
                        result = convert_url_to_tags(current_workflow)
                        if result not in filtered_workflow[key]:
                            filtered_workflow[key].append(result)
                current_workflow.pop()
            # visited_links.pop()

            return parent

        # Loop through new links and add them to the current workflow and visited links
        else:
            for link in a_tags:
                if 'href' in link.attrib.keys():
                    new_url = link.attrib['href']
                    new_tag = assign_tag(new_url)
                else:
                    continue
                if not new_url.startswith('http'):
                    new_url = check_url(new_url)
                    new_url = b_url+'/'+new_url
                # check if internal link
                if new_url is not None and new_url.startswith(b_url):
                    url_for_workflow = new_url.replace(b_url,'')
                    current_workflow.append(new_url)
                    e_id=''
                    e_class=''
                    if 'id' in link.attrib:
                        e_id = link.attrib['id']
                    if 'class' in link.attrib:
                        e_class = link.attrib['class']
                    tree = lxml_tree.getroottree()
                    xpath = tree.getpath(link)
                    child = crawl(new_url, visited_links, current_workflow,parent['id'],new_tag,e_id,e_class,xpath)
                    parent['children'].append(child)

    # remove the parent after all its children are looped through
    if(len(current_workflow)!=0):
        current_workflow.pop()
    # visited_links.pop()
    return parent

visited_links = set()
current_workflow = []
parent1 = crawl(b_url, visited_links, current_workflow,0,'home','id','class','xpath')
f = open("demo5.json", "a")
f.write(json.dumps(parent1))
f.write("\n")
f.close()



