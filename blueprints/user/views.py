from flask import Blueprint, render_template, flash, redirect,jsonify
import requests
from flask import request,redirect,url_for
user = Blueprint('user', __name__, template_folder='templates')
import pymongo
import json
client = pymongo.MongoClient("mongodb+srv://wooshir:vgs41999@items.uxp6f.mongodb.net/test?retryWrites=true&w=majority")
db = client["steam"]

@user.before_request
def beforeRequest():
    if not request.url.startswith('https'):
        return redirect(request.url.replace('http', 'https', 1))

@user.route('/login',  methods=["GET","POST"])
def login():
    
        

        return render_template('user/login.html')

