import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urlparse
import uuid
from lxml import etree
import re
import nltk
nltk.download('wordnet')
from nltk.corpus import wordnet
from difflib import SequenceMatcher




tags = ["home", "login", "about", "contact", "signup","search","admin",'product',"services",'register','sitemap']


patterns = {
    'home': ['index', 'home', 'main'],
    'cart': ['cart', 'basket'],
    'product': ['product', 'item', 'detail'],
    'about': ['about', 'company', 'team'],
    'search': ['search', 'find'],
    'login':['signin','login','sign-in']
}

b_url = 'https://demo-website-drab-three.vercel.app'

def check_url(url):
    # Remove any leading dots or slashes
    cleaned_path = url.lstrip('.\\/')

    # Return the cleaned up path
    return cleaned_path

def get_path(url):
    parsed_url = urlparse(url)
    path = parsed_url.path
    path = path.replace('/', '').replace('\\', '').replace(';', '').replace('#','')
    return path

def check_tag_exists(workflow,tag):
    is_about_tag = False
    for url in workflow:
        # remove session id from url
        url_for_workflow = url.replace(b_url,'')
        session_id_removed = re.sub(r'[;&]jsessionid=[A-Za-z0-9]+', '', url_for_workflow)
        url = re.sub(r'\?(?=.*&)?(sessionid=\d+&?)', '', session_id_removed)
        # first assign tags manually if possible
        if(assign_tag_manually(url)=='other'):
            if assign_tag(url)==tag:
                is_about_tag = True
        else:
            if assign_tag_manually(url)==tag:
                is_about_tag= True
    return is_about_tag

def convert_url_to_tags(workflow):
    workflow_tags = []
    for url in workflow:
        # remove session id from url
        url_for_workflow = url.replace(b_url,'')
        session_id_removed = re.sub(r'[;&]jsessionid=[A-Za-z0-9]+', '', url_for_workflow)
        url = re.sub(r'\?(?=.*&)?(sessionid=\d+&?)', '', session_id_removed)
        # first assign tag manually if possible
        if assign_tag_manually(url)=='other':
            workflow_tags.append(assign_tag(url))
        else:
            workflow_tags.append(assign_tag_manually(url))
    return workflow_tags


def assign_tag_manually(url):
    if(type(url)!=list):
        path = url.lower().split('/')
        # remove the leading slash
        path = path[1:]
    else:
        path = url

    # Check if any of the patterns match the path
    if len(path)>=2:
        return 'other'
    else:
        for category, keywords in patterns.items():
            if any(keyword in path for keyword in keywords):
                return category

    # If no pattern matches, return "other"
    return 'other'



def extract_words(url):
    # remove session id from url
    url_for_workflow = url.replace(b_url,'')
    session_id_removed = re.sub(r'[;&]jsessionid=[A-Za-z0-9]+', '', url_for_workflow)
    url = re.sub(r'\?(?=.*&)?(sessionid=\d+&?)', '', session_id_removed)
    pattern = r'\b\w+\b'
    match = re.search(r'\.\w+$', url)
    if match:
        extension = match.group()
        extensions_removed = url.replace(extension,'')
    else:
        extensions_removed = url
    words = re.findall(pattern, extensions_removed)
    return words
def word_similarity(word1, word2):
    synsets1 = wordnet.synsets(word1)
    synsets2 = wordnet.synsets(word2)
    if synsets1 and synsets2:
        similarity = max(s1.wup_similarity(s2) for s1 in synsets1 for s2 in synsets2)
    else:
        similarity = SequenceMatcher(None, word1, word2).ratio()
    return similarity
def assign_tag(url):
    url = get_path(url)
    words = extract_words(url)
    if not words:
        return "home"
    # first assign tag manually
    manually_assigned_tag = assign_tag_manually(words)
    if(manually_assigned_tag!='other'):
        return manually_assigned_tag
    max_score = 0
    tag = None
    for t in tags:
        scores = [word_similarity(t, w) for w in words]
        if len(scores) > 0:
            avg_score = sum(scores) / len(scores)
        else:
            avg_score = 0  # or whatever default value you want to use
            return 'others'

        if avg_score > max_score:
            max_score = avg_score
            tag = t
    return tag





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
login = False
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
        if not assign_tag(url)=='home':
            current_workflow.pop()
            return parent
        if(len(current_workflow)!=0):
            # if it is a login workflow store it
            for key in filtered_workflow.keys():
                if(check_tag_exists(current_workflow,'login')):
                    result = convert_url_to_tags(current_workflow)
                    if result not in filtered_workflow['login']:
                        filtered_workflow['login'].append(result)
                        f = open("fw.txt", "a")
                        f.write(str(current_workflow))
                        f.write("\n")
                        f.write(str(result))
                        f.write("\n")
                        f.close()
            current_workflow.pop()
        # visited_links.pop()
        return parent

    # Add the URL to the set of visited links
    else:
        visited_links.add(url)
    # Send an HTTP request to the URL and retrieve the response

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
                        result = convert_url_to_tags(current_workflow[2:])
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
filtered_workflow = {'login':[]}
current_workflow = ['https://demo-website-drab-three.vercel.app/index.html']
parent1 = crawl(b_url, visited_links, current_workflow,0,'home','id','class','xpath')
f = open("demo5.json", "a")
f.write(json.dumps(parent1))
f.write("\n")
f.close()

f = open("filteredworkflow1.json", "a")
f.write(str(filtered_workflow))
f.write("\n")
f.close()




