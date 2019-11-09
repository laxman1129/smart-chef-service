import pandas as pd
import spacy
from fuzzywuzzy import fuzz
import re
from nltk.corpus import stopwords
import collections

# class FuzzySearch:
#     def __init__(self):
#         self.data = pd.read_json('data/all_meals.json')
#         self.data = self.data.transpose()
#         self.parser = spacy.load("en_core_web_sm")
#         self.indices = self.data['id']
#         self.titles = self.data['title'].fillna('')
#         self.ingredients = self.data['ingredients'][:].fillna('')
#         self.category = self.data['category'].fillna('')
#         self.area = self.data['area'].fillna('')
#         self.tags = self.data['tags'].fillna('')
#         self.keywords = self.populate_keywords()
#         self.score_index_dict = collections.defaultdict(list)
#
#     def populate_keywords(self):
#         tokens = []
#         for i in range(0, len(self.titles)):
#             token = (list(self.titles)[i]) + ' ' + (' '.join((list(self.ingredients)[i]))) + ' ' + list(self.category)[
#                 i] + ' ' + \
#                     list(self.area)[
#                         i] + ' ' + list(self.tags)[i]
#             tokens.append(token)
#             return tokens
#
#     @staticmethod
#     def pre_process(text):
#         if not text:
#             return ''
#         # remove special characters and digits
#         text = re.sub("(\\d|\\W)+", " ", text)
#         word_list = text.split()
#         filtered_words = [word for word in word_list if word not in stopwords.words('english')]
#         text = ' '.join(filtered_words)
#         return text.strip()
#
#     def term_tokenizer(self, terms):
#         terms = self.pre_process(terms)
#         terms = self.parser(terms)
#         terms = [word.lemma_.lower().strip() for word in terms]
#         return ' '.join(terms)
#
#     def get_ratio(self, search):
#         for item in self.keywords:
#             print(item, self.term_tokenizer(item))
#             ratio = fuzz.token_set_ratio(search, self.term_tokenizer(item))
#             # print(terms.index(item), ratio)
#             # score_index_dict.setdefault(ratio, [])
#             # score_index_dict[ratio].append(terms.index(item))
#             self.score_index_dict[ratio].append(self.keywords.index(item))
#
#     def get_closest_match(self, search):
#         self.get_ratio(search)
#         sorted_keys = list(self.score_index_dict.keys())
#         sorted_keys.sort()
#         sorted_keys.reverse()
#
#         # return self.score_index_dict[sorted_keys[0]]
#
#
# obj = FuzzySearch()
# print(obj.get_closest_match('lamb garlic'))
# print(obj.keywords)

data = pd.read_json('data/all_meals.json')
data = data.transpose()

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
    while len(search_indices) <= 10:
        search_indices.extend(score_index_dict[sorted_keys[i]])
        i = i + 1

    return search_indices[0:count]


def get_titles(items):
    return [list(titles)[x] for x in items]


def get_id(items):
    return [list(indices)[list(titles).index(x)] for x in items]

# searches = get_closest_match('lamb garlic fennel biryani', keywords)
# print(searches)
# print(list(titles))
#
# print([list(titles)[x] for x in searches])

# list(titles).index('Ratatouille')


