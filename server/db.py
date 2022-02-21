from dotenv import load_dotenv
import os
from pymongo import MongoClient
from datetime import datetime as d
from pymongo.errors import ConnectionFailure
load_dotenv()
PASSWORD = os.environ.get("PASSWORD")
USER = os.environ.get("USER")
cluster = None


def connect_db():
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = f"mongodb+srv://{USER}:{PASSWORD}@cluster0.zkivj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    # Create a connection using MongoClient.
    try:
        cluster = MongoClient(CONNECTION_STRING)
        print("The connection was successful")
        return cluster
    except ConnectionFailure:
        print("Server not available")
        return None


def close_connection():
    global cluster
    if cluster == None:
        print("cluster is None")
        return False
    cluster.close()
    print("connection is closed")

    return True


def get_database():
    global cluster
    cluster = connect_db()
    if cluster == None:
        return None
    # Create the database for our chat
    db = cluster['Chat_py']
    return db


def create_user(nickName: str, password: str) -> bool:
    db = get_database()
    if db == None:
        return False
    if not user_exits(nickName, db):
        try:
            db["users"].insert_one({
                "name": nickName,
                "password": password,
                "dateCreate": d.now(),
            })
            print("user added")
            close_connection()
            return True
        except:
            print("Sorry")
    close_connection()
    return False


def user_exits(nickName: str, db) -> bool:
    ans = db["users"].find({"name": nickName})
    for x in ans:
        if x["name"] == nickName:
            return True
    return False


def auth_user(nickName: str, password: str, db):
    ans = db["users"].find({"name": nickName})
    for x in ans:
        if x["name"] == nickName and x["password"] == password:
            return True
    return False


def loginValid(nickName: str, password: str) -> bool:
    db = get_database()
    if db == None:
        return False
    if auth_user(nickName, password, db):
        ans = True
    else:
        ans = False
    close_connection()
    return ans
