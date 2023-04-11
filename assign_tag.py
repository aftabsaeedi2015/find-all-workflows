import re
import nltk
nltk.download('wordnet')
from nltk.corpus import wordnet
from difflib import SequenceMatcher
from extract_path_from_url import get_path
from urllib.parse import urlparse




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


url = "https://demo-website-drab-three.vercel.app/about.html"
words = extract_words(url)
print("Words:", words)
for tag in tags:
    scores = [word_similarity(tag, word) for word in words]
    print(tag, scores)
tag = assign_tag(url)
print("Tag:", tag)
