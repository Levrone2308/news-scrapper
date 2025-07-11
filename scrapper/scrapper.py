import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient("mongodb://mongo:27017/")
db = client["news"]
collection = db["headlines"]

def scrape_inshorts():
    url = "https://inshorts.com/en/read"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    # Headlines are inside <span itemprop="headline">
    headline_tags = soup.select("span[itemprop='headline']")
    headlines = [tag.get_text(strip=True) for tag in headline_tags if tag.get_text(strip=True)]
    return headlines

def save_to_db(data):
    collection.delete_many({})
    collection.insert_many([{"title": headline} for headline in data])

if __name__ == "__main__":
    headlines = scrape_inshorts()
    print(f"Scraped {len(headlines)} headlines")
    print(headlines)
    if headlines:
        save_to_db(headlines)
        print("Saved to DB.")
    else:
        print("No headlines found.")
