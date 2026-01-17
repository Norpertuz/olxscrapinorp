from bs4 import BeautifulSoup
import os
import re
import glob

TYPE_RE = re.compile(r"olx_page_([a-zA-Z0-9]+)")


def parse_price(text):
    """
    Zamienia tekst ceny typu '1 299 zł' na int 1299
    """
    text = text.replace(" ", "")
    nums = re.findall(r"\d+", text)
    return int("".join(nums)) if nums else None


def fetch_offers(max_price=None):
    """
    Pobiera oferty z lokalnych plików olx_page_*.html.
    Jeśli podano max_price, filtruje oferty powyżej tej ceny.
    """
    all_offers = []

    for file in sorted(glob.glob("files/olx_page_*.html")):
        filename = os.path.basename(file)

        m = TYPE_RE.search(filename)
        if not m:
            continue

        offer_type = m.group(1)

        with open(file, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        # selektor dla ofert
        items = soup.select("div[data-cy='l-card']")

        for item in items:
            title_el = item.select_one("h4")
            price_el = item.select_one("p[data-testid='ad-price']")
            href_el = item.select_one("a.css-1tqlkj0")

            if not title_el or not price_el or not href_el:
                continue

            price = parse_price(price_el.text)
            if price is None:
                continue
            if max_price is not None and price > max_price:
                continue

            href = href_el.get("href")
            url = href if href.startswith("http") else "https://www.olx.pl" + href
            olx_id = href.split("-ID")[-1].split(".")[0] if "-ID" in href else href.split("/")[-1]

            all_offers.append({
                "id": olx_id,
                "title": title_el.text.strip(),
                "price": price,
                "url": url,
                "type": offer_type
            })

    return all_offers
