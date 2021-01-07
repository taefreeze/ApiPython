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
from datetime import date, datetime, time, timedelta
import pytz
import time
import date_format
import hashlib

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
    jsonout = {}
    #loop in collections
    for a in connection.db.List.find():
        id = '{0}'.format(a['_id'])
        dict = {'name_eng' : a.get('name_eng'),'name_th' : a.get('name_th'),'api_url' : a.get('api_url'),'params': a.get('param1'),'time' : a.get('time')}
        jsonout[id] = dict
    return jsonout

@app.get("/Logs")
async def Logs():
    jsonout = {}
    for data in connection.db.Logs.find():
        id = '{0}'.format(data['_id'])
        dict = {'Operation' : data.get('Operation'),'name_eng' : data.get('name_eng'),'name_th' : data.get('name_th'),'api_url' : data.get('api_url'),'params': data.get('param1') , 'time': data.get('time')}
        #"{}".format(data.get('time').strftime(fmt[2]))
        jsonout[id] = dict
    return jsonout

# Signup endpoint with the POST method
@app.post("/ApiSignup")
def Signup(name_eng : str, name_th : str, api_url : str, param1 : str):
    is_exists = False
    data = create(name_eng, name_th, api_url, param1)
    dict(data)
    if connection.db.List.find(
        {'name_eng': data['name_eng']}
        ).count() > 0:
        is_exists = True
        #print("Api Already Exists")
        return {"message":"The Name Api Already Exists"}
    elif is_exists == False:
        epoch = time.time()
        data['time'] = epoch
        data['id'] = hashlib.md5(b'epoch').hexdigest()
        connection.db.List.insert_one(data)
        data['Operation'] = 'Create'
        connection.db.Logs.insert_one(data)
        return {"message":"Success Created",data['Operation'] : 'Create',"name_eng": data['name_eng'], "name_th": data['name_th'], "api_url": data['api_url'], "param1": data['param1'],"datetime": data['time']}

@app.post("/Update")
def Update(id : str ,name_eng : str, name_th : str, api_url : str, param1 : str):
    jsonout = {}
    for update in connection.db.List.find({'_id': ObjectId(id)}):
        #find_id = '{0}'.format(update['_id'])
        if update:
            data = create(name_eng, name_th, api_url, param1)
            connection.db.List.update_one({'_id': ObjectId(id)},{'$set': {update['name_eng']: name_eng,update['name_th'] : name_eng},update['api_url'] : api_url,update['param1'] : param1})
            data['time'] = datetime.now() + timedelta(hours=7)
            data['Operation'] = 'Update'
            data['_id'] = id
            connection.db.Logs.insert_one(data)
            dict = {'Operation' : data['Operation'],'name_eng' : data['name_eng'],'name_th' : data['name_th'],'api_url' : data['api_rul'],'param1': data['param1'] , 'time': data['time']}
            jsonout[id] = dict
            return jsonout
        else:
            return {"message":"The ID Api is not Exists"}
        

if __name__ == '__main__':
   uvicorn.run(app, host="0.0.0.0", port=80, debug=True) 