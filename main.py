import os
import glob
from scraper import fetch_offers
from db import init_db, upsert_offer
import subprocess

def download_pages():
    # Wywołanie Twojego skryptu bash
    subprocess.run(["bash", "download.sh"], check=True)

def cleanup_files():
    for file_path in glob.glob(f"files/*"):
    	if os.path.isfile(file_path):
        	os.remove(file_path)

def main():
    # Inicjalizacja bazy
    init_db()

    # Pobranie stron
    download_pages()

    offers = fetch_offers()
    print(f"Znaleziono {len(offers)} ofert:")

    for o in offers:
        print(o)
        upsert_offer(o)  # zapis do bazy i wykrywanie zmian

    # Usuń pobrane pliki
    cleanup_files()

if __name__ == "__main__":
    main()
