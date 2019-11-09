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
