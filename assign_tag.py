import re
import nltk
nltk.download('wordnet')
from nltk.corpus import wordnet
from difflib import SequenceMatcher
from extract_path_from_url import get_path


tags = ["home", "login", "cart", "about", "contact", "signup","search","others","admin","services","gallery","help",'products',"calender","private policy","resources","careers","forum","feedback"]
def extract_words(url):
    pattern = r'\b\w+\b'
    words = re.findall(pattern, url)
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


url = "signinindex.html"
words = extract_words(url)
print("Words:", words)
for tag in tags:
    scores = [word_similarity(tag, word) for word in words]
    print(tag, scores)
tag = assign_tag(url)
print("Tag:", tag)
