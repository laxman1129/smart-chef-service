from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flask_cors import CORS, cross_origin

import requests
import json

import FuzzySearch as fs
import Recommender as rc

app = Flask(__name__)
api = Api(app)


def get_recommendations(recipe_keywords, count=5):
    indexes = fs.get_closest_match(recipe_keywords, count=count)
    print(indexes)
    titles = fs.get_titles(indexes)
    recommendations = rc.get_recommendations(titles[0], count=count)
    recommendation_list = list(recommendations)
    ids = fs.get_id(recommendation_list)
    print(ids)
    recipes =[]
    for id in ids:
        # recipe_found = es.get(index='recipe-index', doc_type='recipe', id=id)
        recipe_found = requests.get(
            'https://smartchef.eastus.cloudapp.azure.com:9200/recipe-index/recipe/' + str(id),
            verify=False)
        print(recipe_found.json()['_source'])
        recipes.append(recipe_found.json()['_source'])

    return recipes


class Test(Resource):
    @cross_origin()
    def get(self):
        return 'connection successful'


class ContentCreator(Resource):
    @cross_origin()
    def post(self):
        json_data = request.get_json(force=True)
        email_request = json_data['emailRequest']

        for req in email_request:
            route = req['route']
            for menuitem in req['menuRequest']['menu']:
                name = menuitem['name']
                i = 0
                for recipe in menuitem['recipes']:
                    title = recipe['title']
                    ingredients = ' '.join(recipe['ingredients'])

                    recipe_keywords = route + ' ' + name + ' ' + title + ' ' + ingredients
                    # pre-process the keywords
                    recipe_keywords = fs.term_tokenizer(recipe_keywords)
                    print(recipe_keywords)
                    recommendations = get_recommendations(recipe_keywords)
                    recipe['recommentions'].extend(recommendations)
                    i = i+1
                    print(len(recipe['recommentions']))

        # print(email_request[0])
        # res = es.index(index='emailrequests-index', doc_type='emailrequests',
        #                body=json.dumps(emailRequest=email_request[0]))
        url = 'https://smartchef.eastus.cloudapp.azure.com:9200/emailrequests-index/emailrequests/'
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        response = requests.post(url, data=json.dumps(email_request[0]), headers=headers, verify=False)
        return json.dumps(email_request[0])


class Recommender(Resource):
    @cross_origin()
    def get(self, query):
        print(query)
        recommendation = get_recommendations(query)
        return jsonify(recommendation)


api.add_resource(Test, '/')
api.add_resource(ContentCreator, '/menu')
api.add_resource(Recommender, '/get_recipe/<string:query>')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int("5000"), debug=True)
