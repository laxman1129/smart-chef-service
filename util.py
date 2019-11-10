# # import recommender.FuzzySearch as fs
# # import recommender.Recommender as rc
#
# import pandas as pd
#
# # indexes = fs.get_closest_match('lamb garlic biryani', count=15)
# # print(indexes)
# #
# # titles = fs.get_titles(indexes)
# # print(titles)
# #
# # recommendations = rc.get_recommendations(titles[0])
# # print(recommendations)
#
# data = pd.read_json('data/email-request.json')
#
#
# for item in data['emailRequest']:
#     route = item['route']
#     for menuitem in item['menuRequest']['menu']:
#         name = menuitem['name']
#         for recipe in menuitem['recipes']:
#             # print(recipe['title'], ' '.join(recipe['ingredients']))
#             title = recipe['title']
#             ingredients = ' '.join(recipe['ingredients'])
#             recipe_keywords = route + ' ' + name + ' ' + title + ' ' + ingredients
#             print(recipe_keywords)


# import requests
#
# print(requests.get('http://0.0.0.0:5000').content)

# import json
#
# with open("data/x.json", "rb") as jfile:
#     jsonstr = jfile.read()
#     data = json.loads(jsonstr)
#     print(data)

# import json
# from numpy.random import seed
# from numpy.random import randint
# seed(43)
# value = randint(5, 50)
# print(value)
#
# all_new_recipes = open('data/all_meals_new.json', 'r')
# d = json.loads(all_new_recipes.read())
# j52981 = open('data/52981.json', 'r')
# d52981 = json.loads(j52981.read())
# d['recipes'].append(d52981)
# j52982 = open('data/52982.json', 'r')
# d52982 = json.loads(j52982.read())
# d['recipes'].append(d52982)
# j52983 = open('data/52983.json', 'r')
# d52983 = json.loads(j52983.read())
# d['recipes'].append(d52983)
# j52984 = open('data/52984.json', 'r')
# d52984 = json.loads(j52984.read())
# d['recipes'].append(d52984)
# # print(d['recipes'])
#
# # print(d['recipes'][0])
# for i in d['recipes'][0]:
#     i['budget'] =str(randint(5, 50))+'AED'
#
# f = open('data/new_recipe.json', 'w')
# json.dump({'recipes': d['recipes']}, f)
