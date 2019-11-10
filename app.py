from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flask_cors import CORS, cross_origin

from elasticsearch import Elasticsearch

import requests
import json

import FuzzySearch as fs
import Recommender as rc

app = Flask(__name__)
api = Api(app)

host = 'https://smartchef.eastus.cloudapp.azure.com'
es = Elasticsearch(hosts=[host], use_ssl=True, verify_certs=False)


# Index — Database
# Datatype — Type of the document
# Id — Id of the document

# Inserting a document:
# Now let's store this document in Elasticsearch
# res = es.index(index='megacorp',doc_type='employee',id=1,body=e1)

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
                for recipe in menuitem['recipes']:
                    title = recipe['title']
                    ingredients = ' '.join(recipe['ingredients'])

                    recipe_keywords = route + ' ' + name + ' ' + title + ' ' + ingredients
                    # pre-process the keywords
                    print(recipe_keywords)
                    indexes = fs.get_closest_match(recipe_keywords, count=15)
                    print(indexes)
                    titles = fs.get_titles(indexes)
                    recommendations = rc.get_recommendations(titles[0])
                    recommendation_list = list(recommendations)
                    ids = fs.get_id(recommendation_list)
                    print(ids)
                    for id in ids:
                        # recipe_found = es.get(index='recipe-index', doc_type='recipe', id=id)
                        recipe_found = requests.get(
                            'https://smartchef.eastus.cloudapp.azure.com:9200/recipe-index/recipe/' + str(id),
                            verify=False)
                        # print(recipe_found.json()['_source'])
                        recipe['recommentions'].append(recipe_found.json()['_source'])

        print(email_request[0])
        # res = es.index(index='emailrequests-index', doc_type='emailrequests',
        #                body=json.dumps(emailRequest=email_request[0]))
        url = 'https://smartchef.eastus.cloudapp.azure.com:9200/emailrequests-index/emailrequests/'
        print(url)
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        response = requests.post(url, data=json.dumps(email_request[0]), headers=headers, verify=False)
        return 'successful'


api.add_resource(Test, '/')
api.add_resource(ContentCreator, '/menu')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int("5000"), debug=True)
