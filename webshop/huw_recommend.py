from flask import Flask, request, session, render_template, redirect, url_for, g
from flask_restful import Api, Resource, reqparse
import os
from pymongo import MongoClient
from dotenv import load_dotenv
from random import randrange

import psycopg2

app = Flask(__name__)
api = Api(app)

# Since we are asked to pass a class rather than an instance of the class to the
# add_resource method, we open the connection to the database outside of the
# Recom class.
connection = psycopg2.connect("dbname=OpisOp user=postgres password=root")

class Collab(Resource):
    def get(self, profileid, cat):
        cursor = connection.cursor()
        print(cat)
        # cursor.execute(f"""
        # SELECT DISTINCT collab_recommendations.product_recommendation FROM collab_recommendations
        # INNER JOIN profiles ON collab_recommendations.segment = profiles.segment
        # INNER JOIN sessions ON profiles.id = sessions.profiles_id
        # INNER JOIN cart ON sessions.browser_id = cart.sessions_profiles_id
        # INNER JOIN products ON products.id = cart.products_id
        # WHERE profiles.id = '{profileid}'
        # AND collab_recommendations.target_audience = products.targetaudience
        # LIMIT 100
        # """)
        # Work in progress
        sql = "SELECT collab_recommendations.product_recommendation FROM collab_recommendations INNER JOIN profiles ON collab_recommendations.segment = profiles.segment WHERE profiles.id = %s AND collab_recommendations.category LIKE %s LIMIT 10"
        cursor.execute(sql,((profileid),'%'+cat+'%'))
        records = cursor.fetchall()
        cursor.close()
        connection.commit()
        return records[randrange(len(records))][0], 200


class Cart(Resource):
    def get(self, productid):
        cursor = connection.cursor()
        cursor.execute(f"""
        SELECT product_recommendation_id
        FROM cart_recommendations
        WHERE product_cart_id = '{productid}'
        LIMIT 1
        """)
        records = cursor.fetchone()
        cursor.close()
        connection.commit()
        print(records[0])
        return records[0], 200

class Period(Resource):
    def get(self):
        cursor = connection.cursor()
        cursor.execute(f"""
        SELECT product_id
        FROM most_bought_period
        WHERE timeperiod = 'Lente'
        LIMIT 5
        """)
        records = cursor.fetchall()
        cursor.close()
        connection.commit()
        record_output = []
        for x in records:
            record_output.append(x[0])

        return record_output, 200


api.add_resource(Collab, "/collab/<string:profileid>/<string:cat>")
api.add_resource(Cart, "/cart/<string:productid>")
api.add_resource(Period, "/period/")