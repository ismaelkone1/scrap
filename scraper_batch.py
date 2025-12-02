import time
import csv
import os
import unicodedata
import undetected_chromedriver as uc

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scraper_google_undetected(requete, region="Belgique", start_page=25, pages=10, pause=4):
    query = f"{requete} {region}"

    options = uc.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--incognito")
    options.add_argument("--start-maximized")

    CHROMIUM_PATH = "/snap/bin/chromium"

    driver = uc.Chrome(
        options=options,
        browser_executable_path=CHROMIUM_PATH
    )

    driver.get("https://www.google.com")
    time.sleep(2)

    try:
        boutons = [
            "//button[contains(., 'Accepter')]",
            "//button[contains(., 'Tout accepter')]",
            "//button[contains(., 'Accept')]",
            "//button[contains(., 'I agree')]",
            "//div[contains(@class,'VfPpkd')]//button"
        ]
        for b in boutons:
            try:
                driver.find_element(By.XPATH, b).click()
                break
            except:
                pass
    except:
        pass

    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "q"))
    )
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    time.sleep(pause)

    for _ in range(start_page - 1):
        try:
            driver.find_element(By.ID, "pnnext").click()
            time.sleep(pause)
        except:
            break

    urls = []

    for _ in range(pages):
        selectors = [
            "div.yuRUbf > a",
            "a[jsname]",
            "a[href][data-ved]"
        ]
        for sel in selectors:
            elements = driver.find_elements(By.CSS_SELECTOR, sel)
            for e in elements:
                href = e.get_attribute("href")
                if href and "http" in href and href not in urls:
                    urls.append(href)

        try:
            driver.find_element(By.ID, "pnnext").click()
        except:
            break

        time.sleep(pause)

    driver.quit()
    return urls


def slugify(value):
    value = str(value)
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode("ascii")
    value = value.lower()
    value = value.replace("'", "")
    for sep in [" ", "/", "\\", ",", ";", "|"]:
        value = value.replace(sep, "_")
    while "__" in value:
        value = value.replace("__", "_")
    return value.strip("_")


def lancer_batch(fichier_arguments="arguments-recherche.txt", dossier_sortie="resultats"):
    # paramètres fixes pour toutes les recherches
    START_PAGE = 20
    PAGES = 20
    PAUSE = 6

    if not os.path.exists(fichier_arguments):
        print(f"Fichier {fichier_arguments} introuvable.")
        return

    if not os.path.exists(dossier_sortie):
        os.makedirs(dossier_sortie)

    with open(fichier_arguments, "r", encoding="utf-8") as f:
        lignes = f.readlines()

    for idx, ligne in enumerate(lignes, start=1):
        ligne = ligne.strip()
        if not ligne or ligne.startswith("#"):
            continue

        try:
            # Format simple : requete | region
            parts = [p.strip() for p in ligne.split("|")]
            if len(parts) < 2:
                print(f"Ligne {idx} ignorée (pas assez de champs) : {ligne}")
                continue

            requete, region = parts[0], parts[1]

            print(f"\n[Ligne {idx}] Requête='{requete}' | Région='{region}' | start_page={START_PAGE} | pages={PAGES} | pause={PAUSE}")

            urls = scraper_google_undetected(
                requete=requete,
                region=region,
                start_page=START_PAGE,
                pages=PAGES,
                pause=PAUSE
            )

            nom_base = f"{slugify(requete)}_{slugify(region)}"
            csv_path = os.path.join(dossier_sortie, f"resultats_{nom_base}.csv")

            with open(csv_path, "w", newline="", encoding="utf-8") as fcsv:
                writer = csv.writer(fcsv)
                writer.writerow(["url"])
                for u in urls:
                    writer.writerow([u])

            print(f" → {len(urls)} URLs enregistrées dans {csv_path}")

        except Exception as e:
            print(f"Erreur sur la ligne {idx} : {ligne}")
            print(e)


if __name__ == "__main__":
    lancer_batch()
