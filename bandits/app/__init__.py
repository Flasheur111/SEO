from flask import Flask, jsonify,render_template, request
from flask.ext.pymongo import PyMongo
from bing_search_api import BingSearchAPI
from random import randint
from bson import Binary, Code
from bson.json_util import dumps
import json

words = []
app = Flask(__name__)
mongo = PyMongo(app)

@app.route('/', methods=['GET'])
def Index():
    print 'test'
    rand = randint(0, 100)
    keyword=GetRandomWord()
    images = FindRandomImages(keyword)
    if rand > 10:
    	tmp_images = FindKnownImages()
    	for i in range(0, 8 - len(tmp_images)):
    		tmp_images.append(images[i])
    	images = tmp_images
    return render_template('index.html', images=images, rand=rand, keyword=keyword)

@app.route('/images/add', methods=['POST'])
def AddImagesUrl():
    insert = { 'mediaurl' : request.json['MediaUrl'],
            'sourceurl' : request.json['SourceUrl'] ,
            'title' : request.json['Title'],
            'count' : '0' }

    images = mongo.db.images.find({ 'mediaurl': request.json['MediaUrl']})
    count = 0
    for image in images:
    	count = int(image['count'])
    count = count + 1
    insert['count'] = count
    mongo.db.images.remove({'mediaurl':request.json['MediaUrl']})
    item = mongo.db.images.insert(insert)
    return jsonify({ 'message': 'ok'})

@app.route('/images/deleteAll', methods=['GET'])
def RemoveAll():
    mongo.db.images.drop()
    return jsonify({ 'message' : 'Delete all images done'})

@app.route('/images/list', methods=['GET'])
def ListImages():
    array_image = []
    for image in mongo.db.images.find().sort('count', -1):
        array_image.append({ 'MediaUrl' : image['mediaurl'],
                             'SourceUrl' : image['sourceurl'],
                             'Title' : image['title'],
                             'count' : image['count']})
    return jsonify({'results' : array_image })


def GetRandomWord():
    randomIndex = randint(0, len(words) - 1)
    return words[randomIndex]

def FindKnownImages():
    images = mongo.db.images.find()
    mediaArray = []
    for image in images:
        mediaArray.append((image['sourceurl'], image['mediaurl'], image['title']))
    return mediaArray

def FindRandomImages(query):
    my_key = "ofiH66W+uTTX65ME7FKhtd2XtgAHxNEljh+700JzqFs"
    mediaArray = []
    bing = BingSearchAPI(my_key)
    params = {'$format': 'json','$top': 8,'$skip': 0}
    results = bing.search(query, params).json()
    for image in results['d']['results']:
        mediaArray.append((image['MediaUrl'], image['SourceUrl'], image['Title']))
    return mediaArray

with open('dataset/fresh_words.csv', 'r') as f:
    for line in f:
    	words.append(line[:-1])
