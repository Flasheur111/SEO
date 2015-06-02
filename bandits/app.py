from flask import Flask, jsonify
from flask.ext.pymongo import PyMongo
from bing_search_api import BingSearchAPI
import json

app = Flask(__name__)
mongo = PyMongo(app)

@app.route('/images/add/<url>', methods=['GET'])
def AddImagesUrl(url):
    insert = { 'url' : url , 'count' : '0' }
    item = mongo.db.images.insert(insert)
    return jsonify(insert)

@app.route('/images/deleteAll', methods=['GET'])
def RemoveAll():
    mongo.db.images.drop()
    return jsonify({ 'message' : 'Delete all images done'})

@app.route('/images/find/<query>', methods=['GET'])
def FindBingImages(query):
    my_key = "rgCqwxBgK2DcUTFjW3DEsljOvVZ0U0I5rBFytYMTfJg="
    mediaArray = []
    bing = BingSearchAPI(my_key)
    params = {'$format': 'json','$skip': 0}
    results = bing.search('image', query, params).json()
    mediaArray = []
    for image in results['d']['results'][0]['Image']:
    	mediaArray.append((image['MediaUrl'], image['SourceUrl']))
    return jsonify({ 'results': mediaArray })

if __name__ == "__main__":
    app.run(debug=True)
