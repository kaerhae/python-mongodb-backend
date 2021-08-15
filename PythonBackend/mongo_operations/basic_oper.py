from pymongo.message import insert
import os

from dotenv import load_dotenv
from pymongo import MongoClient
from bson.objectid import ObjectId

def connect_mongo(database: str, target:str):
  load_dotenv()
  MONGODB_URI = os.environ["MONGODB_URI"]
  client = MongoClient(MONGODB_URI)
  db = client[database]
  results = db[target]

  return results


def fetchAllResults(database: str):
  r = database.find({})
  resultjson = []
  for d in r:
    d['_id'] = str(d['_id'])
    resultjson.append(d)
  return resultjson

def fetchByID( database:str,id: str):
  r = database.find_one({'_id': ObjectId(id)})
  print(r['_id'])
  return r

def addOne(database:str, obj:object):
  print(obj)
  r = database.insert_one(obj)
  saved_id = r.inserted_id
  print(saved_id)
  return saved_id

def deleteOne(database:str, id:str):
  r = database.find_one_and_delete({'_id': ObjectId(id)})
  return r