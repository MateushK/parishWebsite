from datetime import datetime
import os

from pymongo.collection import Collection, ReturnDocument

import flask
from flask import Flask, request, url_for, jsonify
from flask_pymongo import PyMongo
from pymongo.errors import DuplicateKeyError

from model import Post
from objectid import PydanticObjectId


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/parish_database"
app.config["JSON_AS_ASCII"] = False
pymongo = PyMongo(app)

posts: Collection = pymongo.db.posts


@app.route("/posts/", methods=["GET"])
def latest_posts(): 
    """GET latest posts"""
    num_of_posts = 8
    cursor = posts.find().sort("post_id", -1).limit(num_of_posts)

    return {
        "posts": [Post(**doc).to_json() for doc in cursor],
    }



@app.route("/posts/<int:given_id>", methods=["GET"])
def get_article(given_id):
    """GET a post by its ID"""
    this_article = posts.find_one_or_404({"post_id": given_id})
    return Post(**this_article).to_json()
