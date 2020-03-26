from flask import Flask, request, session, render_template, redirect, url_for, g
from flask_restful import Api, Resource, reqparse
import os
from pymongo import MongoClient
from dotenv import load_dotenv

import psycopg2

app = Flask(__name__)
api = Api(app)

# Since we are asked to pass a class rather than an instance of the class to the
# add_resource method, we open the connection to the database outside of the 
# Recom class.
connection = psycopg2.connect("dbname=OpisOp user=postgres password=root")
cursor = connection.cursor()

class Recom(Resource):
    """ This class represents the REST API that provides the recommendations for
    the webshop. At the moment, the API simply returns a random set of products
    to recommend."""
    def get(self, profileid, count):
        print(self)
        print(profileid,count)
        """ This function represents the handler for GET requests coming in
        through the API. It currently returns a random sample of products. """
        # Get collaborative recommendation
        cursor.execute(f"""
        SELECT collab_recommendations.product_recommendation FROM collab_recommendations
        INNER JOIN profiles ON collab_recommendations.segment = profiles.segment
        WHERE profiles.id = '{profileid}'
        LIMIT {1}
        """)
        records = cursor.fetchone()
        print(records[0])
        return records[0], 200

# This method binds the Recom class to the REST API, to parse specifically
# requests in the format described below.
api.add_resource(Recom, "/<string:profileid>/<int:count>")