from flask import Flask, jsonify, render_template
# from api.models.actor import Actor
# from api.models.movie import Movie
# from api.models import country
# from api.lib import db
import psycopg2

# def create_app(database, dbuser, dbpassword):
#     app = Flask(__name__)
    
#     app.config.from_mapping(DATABASE=database,
#                             DBUSER=dbuser,
#                             DBPASSWORD=dbpassword)