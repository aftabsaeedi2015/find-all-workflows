# import requests
# import nltk
# from nltk.downloader import Downloader
# downloader = Downloader()
# downloader.download('wordnet')
# from bs4 import BeautifulSoup
# from urllib.parse import urlparse, urljoin

# # Replace 'example.com' with the actual URL of the website you want to extract URLs from
# url = 'https://parabank.parasoft.com/parabank/index.htm'

# # Set up a list to keep track of visited URLs and a list to store all the extracted links
# visited_urls = []
# links = []

# # Define a function to recursively visit URLs and extract links
# def visit_url(current_url):
#     # If the URL has already been visited, return
#     if current_url in visited_urls:
#         return

#     # Send a GET request to the URL and get the HTML content
#     response = requests.get(current_url)
#     html_content = response.text

#     # Parse the HTML content using Beautiful Soup
#     soup = BeautifulSoup(html_content, 'html.parser')

#     # Find all the 'a' tags in the HTML content and extract the 'href' attribute from each tag
#     for link in soup.find_all('a',href=True):
#         href = link.get('href')
#         if href:
#             print(href)
#             full_url = urljoin(current_url, href)
#             # Add the extracted link to the list of links
#             links.append(full_url)

#             # Recursively visit the extracted link
#             visit_url(full_url)

#     # Add the visited URL to the list of visited URLs
#     visited_urls.append(current_url)

# # Define a function to parse the words in a URL string
# def parse_url(url_string):
#     # Parse the URL string using urlparse
#     parsed_url = urlparse(url_string)

#     # Split the domain name and path into words
#     domain_words = parsed_url.netloc.split('.')
#     path_words = parsed_url.path.split('/')

#     # Concatenate the domain words and path words into a list of all words
#     all_words = domain_words + path_words

#     # Remove any empty strings from the list of words
#     all_words = [word for word in all_words if word]

#     return all_words

# # Parse the words in the initial URL
# url_words = parse_url(url)
# print(url_words)

# # Start by visiting the initial URL
# print('Visiting URL:', url)
# visit_url(url)
# print('Finished visiting URLs')

# # Write the extracted links and their parsed words to a file
# with open('output.txt', 'w') as f:
#     f.write('Extracted links and their parsed words:\n')
#     for link in links:
#         link_words = parse_url(link)
#         f.write(link + '\n')
#         f.write(str(link_words) + '\n')
#         f.write('\n')

# print('Results written to output.txt')
