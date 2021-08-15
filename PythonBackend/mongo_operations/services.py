from pymongo.message import insert
import os

from dotenv import load_dotenv
from pymongo import MongoClient
from bson.objectid import ObjectId

def connect_mongo(database: str, target:str):
  load_dotenv()
  MONGODB_URI = os.environ["MONGODB_URI"]
  try:
    client = MongoClient(MONGODB_URI)
    db = client[database]
    results = db[target]
    return results
  except Exception as e:
    print('Error on connecting mongodb')
    return e

#GET
def fetchAllResults(database: str):
  try:
    r = database.find({})
    resultjson = []
    for d in r:
      d['_id'] = str(d['_id'])
      resultjson.append(d)
    return resultjson
  except Exception as e:
    print('Error on fetching from mongodb')
    return e
# GET :id
def fetchByID( database:str,id: str):
  try:
    r = database.find_one({'_id': ObjectId(id)})
    print(r['_id'])
    return r
  except Exception as e:
    print('Error on fetching from mongodb')
    return e
#POST
def addOne(database:str, obj:object):
  try:
    r = database.insert_one(obj)
    saved_id = r.inserted_id
    print(saved_id)
    return saved_id
  except Exception as e:
    print('Error on inserting in mongodb')
    return e

#DELETE
def deleteOne(database:str, id:str):
  try:
    r = database.find_one_and_delete({'_id': ObjectId(id)})
    return r
  except Exception as e:
    print('Error on deleting object from mongodb')
    return e

#PUT
def modifyOne(database: str, id:str, newObj):
  try:
    r = database.find_one({'_id': ObjectId(id)})
    if(r != None):
      print(r)
      n = { "$set": newObj }
      database.update_one(r,n) 
      return newObj
    else:
      print('No object found')
      return ('No object find with this ID')
  except Exception as e:
    print('Error on modifying object in mongodb')
    return e