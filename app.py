from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flask_cors import CORS, cross_origin

from elasticsearch import Elasticsearch

import FuzzySearch as fs
import Recommender as rc

app = Flask(__name__)
api = Api(app)

host = 'http://smartchef.eastus.cloudapp.azure.com'
es = Elasticsearch(hosts=[host])


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
                        recipe['recommentions'].append(id)
                        # query_body = {
                        #     "query": {
                        #         "match": {
                        #             "some_field": "search_for_this"
                        #         }
                        #     }
                        # }
                        # print(es.search(index="some_index", body=query_body))

        return jsonify(emailRequest=email_request)


api.add_resource(Test, '/')
api.add_resource(ContentCreator, '/menu')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int("5000"), debug=True)
