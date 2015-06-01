from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/Dis/Moi/Bonjour/', methods=['GET'])
def sayhello():
    return jsonify({ 'Message' : 'Hello World !'})

if __name__ == "__main__":
    app.run(debug=True)
