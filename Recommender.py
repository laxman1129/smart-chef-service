import pandas as pd
import re
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
# Import linear_kernel
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity



def pre_process(text):
    # lower
    if isinstance(text, list):
        text = ' '.join(text)
    if not text:
        return ''
    text = text.lower()
    # remove special characters and digits
    text = re.sub("(\\d|\\W)+", " ", text)
    text = ' '.join(set(text.split(' ')))
    word_list = text.split()
    filtered_words = [word for word in word_list if word not in stopwords.words('english')]
    text = ' '.join(filtered_words)
    return text.strip()


def create_soup(x):
    return ''.join(x['ingredients']) + ' ' + ''.join(x['instructions']) + ' ' + ''.join(x['area']) + ' ' + ''.join(
        x['category']) + ' ' + ''.join(x['title'])


metadata = pd.read_json('data/all_meals.json')
metadata = metadata.transpose()
metadata.reset_index(inplace=True)
metadata.index = range(len(metadata))

# Construct a reverse map of indices and recipe titles
title_indices = pd.Series(metadata.index, index=metadata['title']).drop_duplicates()

# Apply clean_data function to your features.
features = ['ingredients', 'instructions', 'area', 'category', 'tags']

for feature in features:
    metadata[feature] = metadata[feature].apply(pre_process)

# Create a new soup feature
metadata['soup'] = metadata.apply(create_soup, axis=1)

# Define a TF-IDF Vectorizer Object. Remove all english stop words such as 'the', 'a'
tfidf = TfidfVectorizer(stop_words='english')
count_matrix2 = tfidf.fit_transform(metadata['soup'])
cosine_sim2 = cosine_similarity(count_matrix2, count_matrix2)


# Function that takes in movie title as input and outputs most similar recipes
def get_recommendations(inp, search_indices=title_indices, search_cosine_sim=cosine_sim2, search_metadata=metadata, count=10):
    # Get the index of the recipe that matches the title
    # print(inp)
    idx = search_indices[inp]
    # print('idx', idx)

    # print(len(cosine_sim))

    # Get the pairwsie similarity scores of all recipes with that recipe
    sim_scores = list(enumerate(search_cosine_sim[idx]))
    #     sim_scores = list(enumerate(cosine_sim[0]))

    # Sort the recipe based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 10 most similar recipes
    sim_scores = sim_scores[0:count]

    # Get the recipe indices
    meal_indices = [i[0] for i in sim_scores]

    # Return the top 10 most similar recipes
    return search_metadata['title'].iloc[meal_indices]

