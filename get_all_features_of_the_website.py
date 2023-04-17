import ast
from urllib.parse import urlparse
import re
import nltk
from nltk.stem import WordNetLemmatizer
import json

# Download any required resources (only needs to be done once)
nltk.download('wordnet')
# create an empty list to store the lists from the file
all_lists = []
b_url='https://demo-website-drab-three.vercel.app'
# open the file
with open('all_workflows.txt', 'r') as f:
    # loop through each line in the file
    try:
        for line in f:
            # use ast.literal_eval() to safely evaluate the string as a list
            list_from_line = ast.literal_eval(line)
            # append the resulting list to the all_lists list
            all_lists.append(list_from_line)
    except:
        print('nothing')
    f.close()




def find_unique_workflows_and_write_to_file(all_lists):
    newlist = []
    duplist = []
    for i in all_lists:
        if i not in newlist:
            newlist.append(i)
    for i in newlist:
        f = open("unique_workflows.txt", "a")
        f.write(str(i))
        f.write("\n")
    f.close()
    return newlist

def categorize_by_second_last_element(lst):
    categories = {}
    for inner_list in lst:
        category_key = inner_list[-2]
        if category_key not in categories:
            categories[category_key] = []
        categories[category_key].append(inner_list)
    return categories


def get_all_categories():
    unique_workflows = find_unique_workflows_and_write_to_file(all_lists)
    categorized_workflows = categorize_by_second_last_element(unique_workflows)
    return categorized_workflows


def update_dictionary_each_feature_has_shortest_workflow(categories):
    for category in categories.keys():
        all_lists = categories[category]
        shortest_list = all_lists[0]  # initialize shortest_list with the first list
        for lst in all_lists:
            if len(lst) < len(shortest_list):
                shortest_list = lst
        categories[category]=shortest_list
    return categories

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
def assign_tag_to_the_url(url):
    words = extract_words(url)
    return produce_word(words)

def produce_word(word_list):
    # Filter the input word list to words with 5 or more letters
    filtered_word_list = [word.lower() for word in word_list if len(word) >= 5]
    # If the filtered word list is empty, return None
    if not filtered_word_list:
        return None
    # Select the first word from the filtered list
    selected_word = nltk.WordNetLemmatizer().lemmatize(filtered_word_list[0])
    return selected_word

def assign_name_to_keys_of_the_dictionary(dictionary):
    old_keys = list(dictionary.keys())
    new_keys = []
    for key in dictionary:
        new_keys.append(assign_tag_to_the_url(key))
    print(new_keys)
    new_dict = {}
    for key, value in dictionary.items():
        if key in old_keys:
            new_key = new_keys[old_keys.index(key)]
            new_dict[new_key] = value
        else:
            new_dict[key] = value
    return new_dict

def write_finalized_workflows_to_a_file(dictionary):
    f = open("shortest_workflow_for_each_feature.json", "a")
    f.write(json.dumps(dictionary))
    f.write("\n")
    f.close()
categories = get_all_categories()
name_of_features_added_to_dictionary = assign_name_to_keys_of_the_dictionary(categories)
finalized_workflows_for_each_feature = update_dictionary_each_feature_has_shortest_workflow(name_of_features_added_to_dictionary)
print(finalized_workflows_for_each_feature)
write_finalized_workflows_to_a_file(finalized_workflows_for_each_feature)
