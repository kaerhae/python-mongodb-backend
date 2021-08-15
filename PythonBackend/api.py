
import sys
import json
from mongo_operations.basic_oper import addOne, connect_mongo, deleteOne, fetchAllResults, fetchByID


import flask
from flask.json import request, jsonify
from werkzeug.exceptions import abort

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
  return "<h1>Template REST API</h1><p>This site is for practice purposes and holds MTI licence</p>"


@app.route('/api/v1/resources/trips/all', methods=['GET'])
def results():
  data = renderResults()
  return jsonify(data)

def renderResults():
  c = connect_mongo('python-mongo', 'trips')
  results = fetchAllResults(c)
  print(results)
  return results

@app.route('/api/v1/resources/trips', methods=['GET'])
def findById():
  if 'id' in request.args:
    id = request.args['id']
    print(id)
  else:
    abort(404)


  c = connect_mongo('python-mongo', 'trips')
  res = fetchByID(c, id)
  res['_id'] = str(res['_id'])
  return jsonify(res)

@app.route('/api/v1/resources/newTrip', methods=['POST'])
def addtrip():
  body_unicode = request.data.decode('utf-8')
  body = json.loads(body_unicode)
  obj = {}

  obj["date_start"] = body["date_start"]
  obj["date_end"] = body["date_end"]
  obj["locations"] = body["locations"]
  obj["kilometers"] = body["kilometers"]
  obj["done"] = body["done"]

  c = connect_mongo('python-mongo', 'trips')
  r = addOne(c, obj)
  res = (str(r))
  return jsonify(res)

@app.route('/api/v1/resources/trips', methods=['DELETE'])
def delete():
  if 'id' in request.args:
    id = request.args['id']
    print(id)
  else:
    abort(404)

  c = connect_mongo('python-mongo', 'trips')
  res = deleteOne(c, id)
  return jsonify(str(res))

@app.errorhandler(404)
def page_not_found(e):
  return "<h1>404</h1><p>The resource could not be found.</p>", 404

app.run()