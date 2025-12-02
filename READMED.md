Parfait ! Voici une **version complète et copiable** de ton README en Markdown, incluant tout ce qu’on a vu : description, installation, usage, fonctionnement et notes.

```markdown
# Google Scraper Batch

Script Python pour récupérer automatiquement les URLs des résultats Google pour plusieurs requêtes et régions, en utilisant **Selenium avec undetected-chromedriver** pour éviter la détection automatique.

---

## Structure du projet

```

.
├── arguments-recherche.txt    # Requêtes et régions à scraper
└── scraper_batch.py           # Script principal

````

---

## Prérequis

- Python 3.10+
- Modules Python :

```bash
pip install selenium undetected-chromedriver
````

* Chromium installé (par défaut : `/snap/bin/chromium`).
  Si Chromium est ailleurs, modifier la variable `CHROMIUM_PATH` dans `scraper_batch.py`.

---

## Préparer le fichier `arguments-recherche.txt`

Chaque ligne correspond à une recherche au format :

```
requete | region
```

Exemple :

```
entreprise de nettoyage | Belgique
plombier chauffagiste | Bruxelles
```

* Les lignes commençant par `#` sont ignorées.
* Les champs doivent être séparés par `|`.

---

## Lancer le scraper

```bash
python3 scraper_batch.py
```

### Paramètres par défaut

* `START_PAGE = 20` : page de départ du scraping
* `PAGES = 20` : nombre de pages à scraper par requête
* `PAUSE = 5` : pause entre les pages (en secondes)

Le script ouvre **une seule instance de Chrome** et parcourt toutes les requêtes listées dans `arguments-recherche.txt`.

---

## Résultats

* Stockés dans le dossier `resultats/` (créé automatiquement s’il n’existe pas)
* Chaque fichier CSV est nommé selon la requête et la région :

```
resultats_entreprise_de_nettoyage_belgique.csv
```

* Chaque CSV contient une colonne unique `url` listant les liens récupérés.
* Les doublons sont automatiquement filtrés.

---

## Fonctionnement interne

1. Ouverture de Chrome via `undetected-chromedriver` pour éviter la détection par Google.
2. Gestion automatique des pop-ups de consentement Google.
3. Recherche pour chaque requête et récupération des URLs des résultats.
4. Exportation des résultats dans des fichiers CSV séparés.

---

## Optimisations et bonnes pratiques

* Augmenter `PAUSE` si Google ralentit ou bloque le scraping.
* Vérifier le chemin de Chromium si le navigateur ne s’ouvre pas.
* Pour gagner du temps, il est possible de paralléliser les recherches en exécutant plusieurs instances simultanément.

---

## Licence

Ce projet est fourni **tel quel**, à usage personnel ou professionnel.
⚠️ Respectez les conditions d’utilisation de Google
