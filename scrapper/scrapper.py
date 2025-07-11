import requests
from bs4 import BeautifulSoup
import json
from pymongo import MongoClient

client = MongoClient("mongodb://mongo:27017/")
db = client["news"]
collection = db["headlines"]

def scrape_bbc():
    url = "https://www.bbc.com/news"
    res = requests.get(url)
    soup = BeautifulSoup(res.content, "html.parser")
    headlines = [item.get_text() for item in soup.select("h3")]
    return headlines

def save_to_db(data):
    collection.delete_many({})
    collection.insert_many([{"title": headline} for headline in data])

if __name__ == "__main__":
    headlines = scrape_bbc()
    save_to_db(headlines)
    print("Scraped and saved.")
