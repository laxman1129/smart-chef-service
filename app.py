from flask import Flask, jsonify, request
from flask_restful import Api, Resource

import FuzzySearch as fs
import Recommender as rc

app = Flask(__name__)
api = Api(app)


class ContentCreator(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        email_request = json_data['emailRequest']

        for req in email_request:
            route = req['route']
            for menuitem in req['menuRequest']['menu']:
                name = menuitem['name']
                for recipe in menuitem['recipes']:
                    # print(recipe['title'], ' '.join(recipe['ingredients']))
                    title = recipe['title']
                    ingredients = ' '.join(recipe['ingredients'])

                    recipe_keywords = route + ' ' + name + ' ' + title + ' ' + ingredients
                    # pre-process the keywords
                    print(recipe_keywords)
                    indexes = fs.get_closest_match(recipe_keywords, count=15)
                    titles = fs.get_titles(indexes)
                    recommendations = rc.get_recommendations(titles[0])
                    print(recommendations)

        return jsonify(emailRequest=email_request)


api.add_resource(ContentCreator, '/menu')

if __name__ == '__main__':
    app.run(debug=True)
