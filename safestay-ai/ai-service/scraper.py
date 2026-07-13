import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.wg-gesucht.de/en/wg-zimmer-in-Berlin.8.0.1.0.html"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.text, "html.parser")

cards = soup.find_all("div", class_="wgg_card offer_list_item")

data = []

for card in cards:

    try:
        title = card.find("h3").get_text(strip=True)

    except:
        title = "N/A"

    try:
        rent = card.find("span", class_="price").get_text(strip=True)

    except:
        rent = "N/A"

    try:
        location = card.find("span", class_="noprint").get_text(strip=True)

    except:
        location = "Berlin"

    data.append({
        "title": title,
        "rent": rent,
        "location": location
    })

df = pd.DataFrame(data)

df.to_csv("berlin_real_listings.csv", index=False)

print(df.head())