import requests
from bs4 import BeautifulSoup

def scrape_quotes_from_website():
    quotes = []
    url = "https://quotes.toscrape.com/"

    while url:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        for quote in soup.find_all("div", class_="quote"):
            text = quote.find("span", class_="text").get_text(strip=True)
            author = quote.find("small", class_="author").get_text(strip=True)
            tags = [tag.get_text(strip=True) for tag in quote.find_all("a", class_="tag")]

            quotes.append({
                "text": text,
                "author": author,
                "tags": tags
            })

        next_page = soup.select_one(".next a")

        url = "https://quotes.toscrape.com" + next_page["href"] if next_page else None

    return quotes
