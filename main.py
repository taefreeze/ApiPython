#Author: Tae Chanwit
#Date: December 23,2020.

from fastapi import FastAPI
from typing import Optional
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
from google.oauth2 import id_token
from google.auth.transport import requests


class NewApiList(Model):
    obj_id = ObjectId()
    email = EmailType(required=True)
    name = StringType(required=True)
    password = StringType(required=True)
    
# An instance of class NewApiList
newList = NewApiList()

# funtion to create and assign values to the instanse of class User created
def create_user(email, username, password):
    newList.obj_id = ObjectId()
    newList.email = email
    newList.name = username
    newList.password = password
    return dict(newList)

# A method to check if the email parameter exists from the users database before validation of details
def email_exists(email):
    exist = True

    # counts the number of times the email exists, if it equals 0 it means the email doesn't exist in the database
    if connection.db.users.find(
        {'email': email}
    ).count() == 0:
        exist = False
        return exist

# Reads user details from database and ready for validation
def check_login_creds(email, password):
    if not email_exists(email):
        activeuser = connection.db.users.find(
            {'email': email}
        )
        for actuser in activeuser:
            actuser = dict(actuser)
            # Converted the user ObjectId to str! so this can be stored into a session(how login works)
            actuser['_id'] = str(actuser['_id'])    
            return actuser



app = FastAPI()

def result(res):
    return {"result":res}

@app.get("/")
async def main():
    return 'Hello World'

@app.get("token")
async def token():
    try:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
        userid = idinfo['sub']
    except ValueError:
    # Invalid token
        pass
    return {"userid" : userid}

# Signup endpoint with the POST method
@app.post("/signup/{email}/{username}/{password}")
def signup(email, username: str, password: str):
    user_exists = False
    data = create_user(email, username, password)

    # Covert data to dict so it can be easily inserted to MongoDB
    dict(data)

    # Checks if an email exists from the collection of users
    if connection.db.List.find(
        {'email': data['email']}
        ).count() > 0:
        user_exists = True
        print("Api Already Exists")
        return {"message":"The Name Api Already Exists"}
    # If the email doesn't exist, create the user
    elif user_exists == False:
        connection.db.List.insert_one(data)
        return {"message":"User Created","email": data['email'], "name": data['name'], "pass": data['password']}

# Login endpoint
@app.get("/login/{email}/{password}")
def login(email, password):
    def log_user_in(creds):
        if creds['email'] == email and creds['password'] == password:
            return {"message": creds['name'] + ' successfully logged in'}
        else:
            return {"message":"Invalid credentials!!"}
    # Read email from database to validate if user exists and checks if password matches
    logger = check_login_creds(email, password)
    if bool(logger) != True:
        if logger == None:
            logger = "Invalid Email"
            return {"message":logger}
    else:
        status = log_user_in(logger)
        return {"Info":status}

if __name__ == '__main__':
   uvicorn.run(app, host="0.0.0.0", port=80, debug=True) 