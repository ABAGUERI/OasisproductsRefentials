import requests
import time
import csv
import os
print(os.getcwd())
FIELDS = [
    'code',
    'product_name',
    'brands',
    'countries',
    'categories',
    'quantity'
]

OUTPUT_FILE = "openfoodfacts_progressive3.csv"

def fetch_products(page_size=1000, total_products=30000):
    url = "https://world.openfoodfacts.org/cgi/search.pl"
    page = 1
    total_fetched = 0
    retry_delay = 10

    if not os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "w", newline="", encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=FIELDS)
            writer.writeheader()

    while total_fetched < total_products:
        params = {
            "search_simple": 1,
            "action": "process",
            "json": 1,
            "page_size": page_size,
            "page": page,
            "fields": ','.join(FIELDS)
        }

        print(f"Fetching page {page}...")
        try:
            response = requests.get(url, params=params)

            if response.status_code == 429:
                print(f"⏳ Trop de requêtes (429). Attente de {retry_delay} secondes...")
                time.sleep(retry_delay)
                retry_delay *= 2  # délai exponentiel
                continue

            if response.status_code != 200:
                print(f"❌ Erreur HTTP {response.status_code} sur la page {page}")
                break

            data = response.json()
            retry_delay = 10  # réinitialise le délai si la page passe

        except Exception as e:
            print(f"Erreur : {e}")
            break

        if 'products' not in data or not data['products']:
            print("Aucun produit trouvé.")
            break

        with open(OUTPUT_FILE, "a", newline="", encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=FIELDS)
            for product in data['products']:
                writer.writerow({field: product.get(field, "") for field in FIELDS})
                total_fetched += 1
                if total_fetched >= total_products:
                    break

        print(f"✔ Page {page} ajoutée. Total : {total_fetched}")
        page += 1
        time.sleep(3)  # limite la fréquence des appels

    print(f"\n✅ Terminé. {total_fetched} produits enregistrés dans {OUTPUT_FILE}")


if __name__ == "__main__":
    fetch_products()
