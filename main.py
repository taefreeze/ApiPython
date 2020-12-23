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

app = FastAPI()

def result(res):
    return {"result":res}
@app.get("/")
async def main():
    return 'Hello World'

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


if __name__ == '__main__':
   uvicorn.run(app, host="0.0.0.0", port=80, debug=True) 