import time
import csv
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scraper_google_undetected(requete, region="Belgique", start_page=25, pages=10, pause=4):

    query = f"{requete} {region}"

    # --- OPTIONS CHROMIUM LINUX ---
    options = uc.ChromeOptions()

    # IMPORTANT SOUS LINUX / CHROMIUM
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--incognito")
    options.add_argument("--start-maximized")

    # 👉 CHANGE ICI AVEC LE CHEMIN RETOURNÉ PAR "which chromium"
    CHROMIUM_PATH = "/snap/bin/chromium"     # ← METS TON CHEMIN ICI

    driver = uc.Chrome(
        options=options,
        browser_executable_path=CHROMIUM_PATH
    )

    # --- SCRAPING GOOGLE ---
    driver.get("https://www.google.com")
    time.sleep(2)

    # Accepter les cookies
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

    # Requête
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "q"))
    )
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    time.sleep(pause)

    # Aller à la page de départ
    for _ in range(start_page - 1):
        try:
            driver.find_element(By.ID, "pnnext").click()
            time.sleep(pause)
        except:
            break

    urls = []

    # Scraping des pages suivantes
    for _ in range(pages):

        # sélection de liens organiques
        selectors = [
            "a[jsname]",
            "div.yuRUbf > a",
            "a[href][data-ved]"
        ]

        for sel in selectors:
            elements = driver.find_elements(By.CSS_SELECTOR, sel)
            for e in elements:
                href = e.get_attribute("href")
                if href and "http" in href and href not in urls:
                    urls.append(href)

        # Page suivante
        try:
            driver.find_element(By.ID, "pnnext").click()
        except:
            break

        time.sleep(pause)

    driver.quit()
    return urls


# ----------------------------------------------------------
#  APPEL DE LA FONCTION + EXPORT CSV
# ----------------------------------------------------------

urls = scraper_google_undetected(
    requete="electricien",
    region="Wallonie",
    start_page=25,
    pages=10,
    pause=3
)

# Export CSV
with open("resultats_google_electricien.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["url"])
    for u in urls:
        writer.writerow([u])

print("Terminé :", len(urls), "URLs enregistrées dans resultats_google.csv")
