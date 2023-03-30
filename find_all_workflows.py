import requests
from bs4 import BeautifulSoup
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from urllib.parse import urlparse
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from assign_tag import assign_tag
from check_tag_exists import check_tag_exists
from check_tag_exists import convert_url_to_tags
from valid_url import check_url
import uuid
from lxml import etree

# from screenshot import get_screenshot



# Initialize the Selenium web driver
# service = Service('./chromedriver')
# chrome_options = Options()
# chrome_options.add_argument('--headless')
# # create a new instance of the Chrome driver
# driver = webdriver.Chrome(options=chrome_options)
# driver = webdriver.Chrome(service=service)

b_url = 'https://parabank.parasoft.com/parabank/index.htm'



def generate_unique_id():
    return str(uuid.uuid4())
login = False
def crawl(url, visited_links, current_workflow,parent_id,tag,e_id,e_class,e_xpath):
    login = False
    parent = {
        'id': generate_unique_id(),
        'url': url,
        'locators':[{'id':e_id,'class':e_class,'xpath':e_xpath}],
        'tag':tag,
        'parent_id':parent_id,
        'children': []
    }
    if url in visited_links:
        # Remove the current link from the current workflow and return
        if(len(current_workflow)!=0):
            current_workflow.pop()
            # if it is a login workflow store it

            if(check_tag_exists(current_workflow,'about')):
                result = convert_url_to_tags(current_workflow)
                f = open("about.txt", "a")
                f.write(str(result))
                f.write(str(current_workflow))
                f.write("\n")
                f.close()
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
                current_workflow.pop()
                if(check_tag_exists(current_workflow,'about')):
                    result = convert_url_to_tags()
                    f = open("about.txt", "a")
                    f.write(str(result))
                    f.write(str(current_workflow))
                    f.write("\n")
                    f.close()
            return parent

        # Loop through new links and add them to the current workflow and visited links
        else:
            for link in a_tags:
                new_url = link.attrib['href']
                new_tag = assign_tag(new_url)
                if not new_url.startswith('http'):
                    new_url = check_url(new_url)
                    new_url = b_url+'/'+new_url
                # check if internal link
                if new_url is not None and new_url.startswith(b_url):
                    url_for_workflow = new_url.replace(b_url,'')
                    current_workflow.append(url_for_workflow)
                    # check if attribute exists
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

    return parent

visited_links = set()
current_workflow = ['/parabank/index.htm']
parent1 = crawl(b_url, visited_links, current_workflow,0,'home','id','class','xpath')
f = open("demo4.json", "a")
f.write(json.dumps(parent1))
f.write("\n")
f.close()

f = open("visitedlinks.txt", "a")
f.write(str(visited_links))
f.write("\n")
f.close()




