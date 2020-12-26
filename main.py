#Author: Tae Chanwit
#Date: December 23,2020.

from fastapi import FastAPI
from typing import List, Optional
import connection
import uvicorn
import numpy as np
from bson import ObjectId
import re
import math
import requests
from bs4 import BeautifulSoup
from fastapi.responses import PlainTextResponse
from collections import Counter
from schematics.models import Model
from schematics.types import StringType, EmailType
from fastapi.middleware.cors import CORSMiddleware
import os
from pymongo import MongoClient
from datetime import datetime

class NewApiList(Model):
    obj_id = ObjectId()
    name_eng = StringType(required=True)
    name_th = StringType(required=True)
    api_url = StringType(required=True)
    param1 = StringType(required=True)
    
# An instance of class NewApiList
newList = NewApiList()

# funtion to create and assign values to the instanse of class User created
def create(name_eng, name_th, api_url, param1):
    newList.obj_id = ObjectId()
    newList.name_eng = name_eng
    newList.name_th = name_th
    newList.api_url = api_url
    newList.param1 = param1
    return dict(newList)

app = FastAPI()

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def result(res):
    return {"result":res}
@app.get("/")
async def main():
    return 'Hello World'

@app.get("/ApiList")
async def ApiList():
    #create dict for stored data in collections
    #jsonout = list(connection.db.List.find({},{_id:0}))
    jsonout = {}
    #loop in collections
    for a in connection.db.List.find():
        id = '{0}'.format(a['_id'])
        dict = {'name_eng' : a.get('name_eng'),'name_th' : a.get('name_th'),'api_url' : a.get('api_url'),'params': a.get('param1')}
        jsonout[id] = dict
    return jsonout

# Signup endpoint with the POST method
@app.post("/ApiSignup")
def Signup(name_eng : str, name_th : str, api_url : str, param1 : str):
    is_exists = False
    data = create(name_eng, name_th, api_url, param1)
    # Covert data to dict so it can be easily inserted to MongoDB
    dict(data)
    # Checks if an email exists from the collection of users
    if connection.db.List.find(
        {'name_eng': data['name_eng']}
        ).count() > 0:
        is_exists = True
        print("Api Already Exists")
        return {"message":"The Name Api Already Exists"}
    # If the email doesn't exist, create the user
    elif is_exists == False:
        connection.db.List.insert_one(data)
        data['time'] = datetime.now()
        connection.db.Logs.insert_one(data)
        return {"message":"Success Created","name_eng": data['name_eng'], "name_th": data['name_th'], "api_url": data['api_url'], "param1": data['param1'],"datetime": data['time']}


if __name__ == '__main__':
   uvicorn.run(app, host="0.0.0.0", port=80, debug=True) 