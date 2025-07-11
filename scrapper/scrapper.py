import requests
from bs4 import BeautifulSoup
import json
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://mongo:27017/")
db = client["news"]
collection = db["headlines"]

# Function to scrape BBC News
def scrape_inshorts():
    url = "https://inshorts.com/en/read"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.content, "html.parser")

    headline_tags = soup.select("div.news-card-title span")
    headlines = [tag.get_text(strip=True) for tag in headline_tags if tag.get_text(strip=True)]
    return headlines




# Save headlines to MongoDB
def save_to_db(data):
    collection.delete_many({})
    collection.insert_many([{"title": headline} for headline in data])

# Main execution
if __name__ == "__main__":
    headlines = scrape_inshorts()
    print(f"Scraped {len(headlines)} headlines")
    print(headlines)
    if headlines:
        save_to_db(headlines)
        print("Saved to DB.")
    else:
        print("No headlines found.")
