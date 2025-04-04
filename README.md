# 🌍 OpenFoodFacts Product Extractor

Ce script Python permet de récupérer automatiquement des données de produits alimentaires à partir de l'API publique d’[OpenFoodFacts](https://world.openfoodfacts.org/) et de les enregistrer dans un fichier CSV local.

## 📦 Fonctionnalités

- Télécharge jusqu'à 30 000 produits depuis l’API OpenFoodFacts.
- Récupère des champs clés : `code`, `product_name`, `brands`, `countries`, `categories`, `quantity`.
- Gère les erreurs de connexion, les délais entre les appels et les erreurs de type 429 (trop de requêtes).
- Reprend le téléchargement dans un fichier CSV existant.

## 🐍 Dépendances

Le script utilise uniquement des bibliothèques standard, sauf pour :

```bash
pip install requests
```

## 🛠️ Utilisation

Exécute simplement le script depuis un terminal :

```bash
python openfoodfacts_downloader.py
```

Tu peux modifier les paramètres `page_size` ou `total_products` dans la fonction `fetch_products()` pour ajuster la quantité de données téléchargées.

## 🧾 Fichier de sortie

Les données sont enregistrées dans un fichier CSV nommé :

```text
openfoodfacts_progressive3.csv
```

Chaque ligne du fichier représente un produit, avec les colonnes suivantes :
- `code` : code-barres du produit
- `product_name` : nom du produit
- `brands` : marque(s)
- `countries` : pays où le produit est vendu
- `categories` : catégories nutritionnelles
- `quantity` : quantité (ex. 500g, 1L)

## 🧠 Remarques techniques

- Le script utilise une pagination et ajoute progressivement les données dans le fichier CSV (mode `append`).
- En cas de trop nombreuses requêtes (`HTTP 429`), il attend un délai croissant avant de réessayer (backoff exponentiel).
- Une pause de 3 secondes est prévue entre chaque appel pour respecter les limitations de l’API.

## ✅ Exemple de résultat

```csv
code,product_name,brands,countries,categories,quantity
3560070978323,Pâtes complètes,Barilla,France,Pâtes,500g
...
```

## 👨‍💻 Auteur

Ce script a été développé pour faciliter la création d’une base de données de produits alimentaires, notamment dans le cadre de projets de gestion de stock ou d’analyse nutritionnelle.
