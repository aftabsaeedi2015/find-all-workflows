from urllib.parse import urlparse

def get_path(url):
    parsed_url = urlparse(url)
    path = parsed_url.path
    path = path.replace('/', '').replace('\\', '').replace(';', '').replace('#','')
    return path

# Example usage:
url = 'https://www.anything.com/actions/Catalog.action?viewProduct=&productId=FL-DSH-01'
path = get_path(url)
print(path)
