from flask import Flask, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient("mongodb://mongo:27017/")
db = client["news"]
collection = db["headlines"]

@app.route("/headlines", methods=["GET"])
def get_headlines():
    headlines = list(collection.find({}, {"_id": 0}))
    return jsonify(headlines)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
