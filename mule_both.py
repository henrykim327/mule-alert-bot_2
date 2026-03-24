import requests
from bs4 import BeautifulSoup
import re

WEBHOOK_URL = "https://discord.com/api/webhooks/1486040772783505478/TYWSxGxQJdHtk6QBM2cDfN3gdwrHoYSFEF1soHs546PQzqzR3kuZ24KBdL379dR85kvx"

URL = "https://www.mule.co.kr/bbs/market/guitar"

KEYWORDS = {
    "THR10II": 350000,
    "THR10": 250000
}

def get_price(text):
    numbers = re.findall(r'\d+', text)
    if numbers:
        return int(numbers[0]) * 10000
    return None

def send_discord(title, link, price):
    data = {
        "content": f"매물 발견!\n{title}\n가격: {price}원\n{link}"
    }
    requests.post(WEBHOOK_URL, json=data)

def check_mule():
    res = requests.get(URL)
    soup = BeautifulSoup(res.text, "html.parser")

    posts = soup.select("a.subject")

    for post in posts:
        title = post.text.strip()
        link = "https://www.mule.co.kr" + post.get("href")

        for keyword, max_price in KEYWORDS.items():
            if keyword in title:
                price = get_price(title)
                if price and price <= max_price:
                    send_discord(title, link, price)

check_mule()
