import pandas as pd
import spacy
from fuzzywuzzy import fuzz
import re
from nltk.corpus import stopwords
import collections
import pickle
import os.path

if os.path.exists('data/datafile.pickle'):
    infile = open('data/datafile.pickle', 'rb')
    data = pickle.load(infile)
    infile.close()
    print('read')
else:
    data = pd.read_json('data/all_meals.json')
    data = data.transpose()
    outfile = open('data/datafile.pickle', 'wb')
    pickle.dump(data, outfile)
    outfile.close()
    print('write')

parser = spacy.load("en_core_web_sm")

indices = data['id']
titles = data['title'].fillna('')
ingredients = data['ingredients'][:].fillna('')
category = data['category'].fillna('')
area = data['area'].fillna('')
tags = data['tags'].fillna('')

keywords = []


def populate_keywords():
    for i in range(0, len(titles)):
        tokens = (list(titles)[i]) + ' ' + (' '.join((list(ingredients)[i]))) + ' ' + list(category)[i] + ' ' + \
                 list(area)[
                     i] + ' ' + list(tags)[i]
        keywords.append(tokens)


populate_keywords()


def pre_process(text):
    if not text:
        return ''
    # text = text.lower()
    # remove special characters and digits
    text = re.sub("(\\d|\\W)+", " ", text)
    word_list = text.split()
    filtered_words = [word for word in word_list if word not in stopwords.words('english')]
    text = ' '.join(filtered_words)
    return text.strip()


def term_tokenizer(terms):
    terms = pre_process(terms)
    terms = parser(terms)
    terms = [word.lemma_.lower().strip() for word in terms]
    return ' '.join(terms)


score_index_dict = collections.defaultdict(list)


def get_ratio(search, terms):
    for item in terms:
        # print(item, term_tokenizer(item))
        ratio = fuzz.token_set_ratio(search, term_tokenizer(item))
        # print(terms.index(item), ratio)
        # score_index_dict.setdefault(ratio, [])
        # score_index_dict[ratio].append(terms.index(item))
        score_index_dict[ratio].append(terms.index(item))


def get_closest_match(search, terms=keywords, count=10):
    get_ratio(search, terms)
    sorted_keys = list(score_index_dict.keys())
    sorted_keys.sort()
    sorted_keys.reverse()
    search_indices = []
    i = 0;
    while len(search_indices) <= count:
        search_indices.extend(score_index_dict[sorted_keys[i]])
        i = i + 1

    return search_indices[0:count+1]


def get_titles(items):
    return [list(titles)[x] for x in items]


def get_id(items):
    return [list(indices)[list(titles).index(x)] for x in items]

