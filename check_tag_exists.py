from assign_tag import assign_tag
from urllib.parse import urlparse


patterns = {
    'home': ['index', 'home', 'main'],
    'cart': ['cart', 'basket'],
    'product': ['product', 'item', 'detail'],
    'about': ['about', 'contact', 'company', 'team'],
    'search': ['search', 'find'],
    'login':['signin','login','sign-in']
}

b_url = 'https://parabank.parasoft.com/parabank/index.htm'


def check_tag_exists(workflow,tag):
    is_about_tag = False
    for url in workflow:
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
        # first assign tag manually if possible
        if assign_tag_manually(url)=='other':
            workflow_tags.append(assign_tag(url))
        else:
            workflow_tags.append(assign_tag_manually(url))
    return workflow_tags

def assign_tag_manually(url):
    path = url.lower().split('/')
    # remove the leading slash
    path = path[1:]

    # Check if any of the patterns match the path
    if len(path)>=2:
        return 'other'
    else:
        for category, keywords in patterns.items():
            if any(keyword in path for keyword in keywords):
                return category

    # If no pattern matches, return "other"
    return 'other'


