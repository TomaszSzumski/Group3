"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

from flask import Flask, render_template, request
import pymongo
from pymongo import MongoClient
import werkzeug
from bson.json_util import dumps
import json
import datetime
import sys
import dns
from flask_table import Table, Col
from collections import defaultdict


app = Flask(__name__)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app
#connecting to mongodb
try:
 client = pymongo.MongoClient("mongodb+srv://ozan:kaya@cluster0.2v7o6.mongodb.net/<dbname>?retryWrites=true&w=majority")
 print("Connected to cruise MongoClient Successfully from Project Script!!!")
except:
 print("Connection to MongoClient Failed!!!")

db=client["cruise_db"]
col = db["cruise_records"]
cur = col.find()
mydict = dict()
headers = ["Cruise", "Destination", "Offer", "Offer_Availability", "Special", "Conditions", "Period", "Time", "Special_Price", "Full_Price"]
rows = []
f = col.find()
for doc in f:
    row_count = len(doc[headers[0]].keys())
    for i in range(row_count):
        row = []
        for header in headers:
            row.append(doc[header][str(i)])
        rows.append(row)
print(rows)


#home page
@app.route("/")

def home():
  return render_template("home.html")

#getting raw data from mongodb to database
@app.route("/data")
def results():
    try:
        Project_List_Col = col.find()
        return render_template('results.html',holidays=rows)
    except Exception as e:
        return dumps({'error': str(e)})





@app.route("/about")
def about():
  return render_template("about.html")

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
