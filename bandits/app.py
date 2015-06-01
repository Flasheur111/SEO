from flask import Flask, jsonify
from flask.ext.pymongo import PyMongo
app = Flask(__name__)
mongo = PyMongo(app)

@app.route('/images/add/<url>', methods=['GET'])
def AddImagesUrl(url):
    insert = { 'url' : url , 'count' : '0' }
    item = mongo.db.images.insert(insert)
    return jsonify({ 'id' : str(item), 'url' : url, 'count': '0' })

@app.route('/images/deleteAll', methods=['GET'])
def RemoveAll():
    mongo.db.images.drop()
    return jsonify({ 'message' : 'Delete all images done'})

if __name__ == "__main__":
    app.run(debug=True)
