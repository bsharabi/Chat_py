import sys
sys.path.append("./Server")
from dotenv import load_dotenv
import os
from pymongo import MongoClient
from datetime import datetime as d
from pymongo.errors import ConnectionFailure
load_dotenv()
PASSWORD = os.environ.get("PASSWORD")
USER = os.environ.get("USER")
cluster = None


class mongodb:

    def __init__(self, nameDB: str = "") -> None:
        self.__cluster = None
        self.name = nameDB
        self.db = None

    def connect_db(self)->bool:
        # Provide the mongodb atlas url to connect python to mongodb using pymongo
        CONNECTION_STRING = f"mongodb+srv://{USER}:{PASSWORD}@cluster0.zkivj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
        # Create a connection using MongoClient.
        try:
            self.__cluster = MongoClient(CONNECTION_STRING)
            print("The connection was successful")
            self.db = self.__cluster[self.name]
            return True
        except ConnectionFailure:
            print("The connection failed")
        return False

    def close_connection(self):
        if self.__cluster == None:
            print("cluster is None")
            return False
        try:
            self.__cluster.close()
            print("connection is closed")
            self.db = None
            self.__cluster = None
            return True
        except:
            print("Failed to close connection")
            return False

    def create_user(self, *args, **kwargs) ->  bool:
        if self.db == None:
            print("Failed to create user, connection failed")
            return False
        try:
            ObjId = self.db["Users"].insert_one(kwargs)
            print("Successful user creation ", ObjId)
            return True
        except:
            print("Failed to create user")
            return False

    def user_exits(self, *args, **kwargs) -> tuple[bool, str]:
        try:
            users = self.db["Users"].find({"UserName":kwargs["UserName"]})
            for user in users:
                if user["UserName"] == kwargs["UserName"]:
                    return True, "User exist"
        except:
            print("User search failed")
            return False, "faild"
        return False, "D-exist"

    def auth_user(self, *args, **kwargs):
        try:
            users = self.db["Users"].find({"UserName": kwargs["UserName"]})
            
            for user in users:
                if user["UserName"] == kwargs["UserName"] and user["UserPassword"] == kwargs["UserPassword"]:
                    return True, "match"
        except:
            print("User search failed")
            return False, "faild"
        print("User auth faild ")
        return False, "D-match"

    def loginValid(self, *args, **kwargs) -> bool:
        pass
