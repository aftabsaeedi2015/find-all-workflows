from urllib.parse import urlparse

def get_path(url):
    parsed_url = urlparse(url)
    path = parsed_url.path
    path = path.replace('/', '').replace('\\', '').replace(';', '').replace('#','')
    return path

# Example usage:
url = 'https://www.anything.com/login/index.html'
path = get_path(url)
print(path)
