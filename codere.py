from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import csv

competition_selectors = [
    "#nav > page-calendar > ion-grid > ion-row > ion-col > ion-content > div.scroll-content > div:nth-child(2) > sb-dropdown > div.sb-dropdown--header.background-color-regular.color-dark",
    "#nav > page-calendar > ion-grid > ion-row > ion-col > ion-content > div.scroll-content > div:nth-child(3) > sb-dropdown > div.sb-dropdown--header.background-color-regular.color-dark"
    # Agrega el resto de los selectores aquí
]

def webscraping(url, league_button_selector):
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
    driver = webdriver.Chrome('chromedriver', options=options)
    driver.get(url)

    # Hacer clic en el botón de "OK" en la ventana emergente de cookies
    cookies_ok_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "body > ion-app > ion-alert > div > div.alert-button-group > button > span"))
    )
    cookies_ok_button.click()

    # Hacer clic en el botón de LaLiga
    league_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, league_button_selector))
    )
    league_button.click()

    data = []

    i = 1
    no_elements_count = 0

    while True:
        found_elements = False
        try:
            equipos_selector = f"#nav > event-page > ion-content > div.scroll-content > div:nth-child(2) > ion-list > sb-grid-item:nth-child({i}) > div > div.sb-grid-item--content > sb-grid-content-teams > div > p"
            cuotas_selector = f"#nav > event-page > ion-content > div.scroll-content > div:nth-child(2) > ion-list > sb-grid-item:nth-child({i}) > div > div:nth-child(2) > div.sb-grid-item--bets-group.has-2-groups.is-wrap.has-three-buttons > sb-button > div > p.sb-button--subtitle.color-dark"

            equipos_elements = WebDriverWait(driver, 3).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, equipos_selector))
            )

            cuotas_elements = WebDriverWait(driver, 3).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, cuotas_selector))
            )

            equipos = [element.text for element in equipos_elements]
            cuotas = [element.text for element in cuotas_elements]

            partido = {
                "equipo1": equipos[0],
                "equipo2": equipos[1],
                "cuota1": cuotas[0],
                "cuotaX": cuotas[1],
                "cuota2": cuotas[2]
            }
            data.append(partido)
            found_elements = True

        except TimeoutException:
            no_elements_count += 1
            if no_elements_count >= 5:  # Break the loop if no elements found in 5 consecutive iterations
                break
        else:
            no_elements_count = 0

        i += 1

    driver.quit()
    return data

def webscraping_nba(url, league_button_selector):
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
    driver = webdriver.Chrome('chromedriver', options=options)
    driver.get(url)

    cookies_ok_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "body > ion-app > ion-alert > div > div.alert-button-group > button > span"))
    )
    cookies_ok_button.click()

    league_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, league_button_selector))
    )
    league_button.click()

    data = []

    i = 1
    no_elements_count = 0

    while True:
        found_elements = False
        try:
            equipos_selector = f"#nav > event-page > ion-content > div.scroll-content > div:nth-child(2) > ion-list > sb-grid-item:nth-child({i}) > div > div.sb-grid-item--content > sb-grid-content-teams > div > p"
            cuotas_selector = f"#nav > event-page > ion-content > div.scroll-content > div:nth-child(2) > ion-list > sb-grid-item:nth-child({i}) > div > div:nth-child(2) > div:nth-child(1) > sb-button:nth-child(1) > div > p.sb-button--subtitle.color-dark, #nav > event-page > ion-content > div.scroll-content > div:nth-child(2) > ion-list > sb-grid-item:nth-child({i}) > div > div:nth-child(2) > div:nth-child(1) > sb-button:nth-child(2) > div > p.sb-button--subtitle.color-dark"


            equipos_elements = WebDriverWait(driver, 3).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, equipos_selector))
            )

            cuotas_elements = WebDriverWait(driver, 3).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, cuotas_selector))
            )

            equipos = [element.text for element in equipos_elements]
            cuotas = [element.text for element in cuotas_elements]

            partido = {
                "equipo1": equipos[0],
                "equipo2": equipos[1],
                "cuota1": cuotas[0],
                "cuotaX": None,  # No hay cuotaX en la NBA
                "cuota2": cuotas[1]
            }
            data.append(partido)
            found_elements = True

        except TimeoutException:
            no_elements_count += 1
            if no_elements_count >= 5:  # Break the loop if no elements found in 5 consecutive iterations
                break
        else:
            no_elements_count = 0

        i += 1

    driver.quit()
    return data

def webscraping_tenis(url, tennis_button_selector, competition_selectors):
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
    driver = webdriver.Chrome('chromedriver', options=options)
    driver.get(url)

    # Hacer clic en el botón de "OK" en la ventana emergente de cookies
    cookies_ok_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "body > ion-app > ion-alert > div > div.alert-button-group > button > span"))
    )
    cookies_ok_button.click()

    # Hacer clic en el botón de Tenis
    tennis_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, tennis_button_selector))
    )
    tennis_button.click()

    # Hacer clic en el botón de Tenis en la siguiente página
    tennis_button2_selector = "#nav > page-calendar > ion-grid > ion-row > ion-col > ion-content > div.scroll-content > div.sb-sticky > sb-filter > div > div > div.swiper-slide.sb-filter-item.swiper-slide-next > span"
    try:
        tennis_button2 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, tennis_button2_selector))
        )
        tennis_button2.click()
    except TimeoutException:
        print("El botón tennis_button2 no se encontró. Continuando con el proceso.")


    # Hacer clic en todos los botones de competición
    for selector in competition_selectors:
        try:
            # Wait for the element to be re-attached to the DOM
            competition_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )

            # Wait for the element to be clickable
            competition_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
            )

            competition_button.click()
        except TimeoutException:
            print(f"No se pudo hacer clic en el botón de la competición con selector {selector}")

    # Extraer los datos de los partidos de tenis
    data = []
    i = 1
    no_elements_count = 0

    while True:
        found_elements = False
        try:
            equipos_selector = f"#nav > event-page > ion-content > div.scroll-content > div:nth-child(2) > ion-list > sb-grid-item:nth-child({i}) > div > div.sb-grid-item--content > sb-grid-content-teams > div > p"
            cuotas_selector = f"#nav > event-page > ion-content > div.scroll-content > div:nth-child(2) > ion-list > sb-grid-item:nth-child({i}) > div > div:nth-child(2) > div:nth-child(1) > sb-button:nth-child(1) > div > p.sb-button--subtitle.color-dark, #nav > event-page > ion-content > div.scroll-content > div:nth-child(2) > ion-list > sb-grid-item:nth-child({i}) > div > div:nth-child(2) > div:nth-child(1) > sb-button:nth-child(2) > div > p.sb-button--subtitle.color-dark"

            equipos_elements = WebDriverWait(driver, 3).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, equipos_selector))
            )

            cuotas_elements = WebDriverWait(driver, 3).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, cuotas_selector))
            )

            equipos = [element.text for element in equipos_elements]
            cuotas = [element.text for element in cuotas_elements]

            partido = {
                "equipo1": equipos[0],
                "equipo2": equipos[1],
                "cuota1": cuotas[0],
                "cuota2": cuotas[1]
            }
            data.append(partido)
            found_elements = True

        except TimeoutException:
            no_elements_count += 1
            if no_elements_count >= 5:  # Break the loop if no elements found in 5 consecutive iterations
                break
            else:
                no_elements_count = 0

            i += 1

        driver.quit()
        return data

url = input("Por favor, ingrese la URL: ")

laliga_button_selector = "body > ion-app > ng-component > ion-grid > ion-row > ion-col.menu-web.prueba-1.col > codere-sidebar-pc > div > ion-list.menuLatDestacados.list.list-md > ion-item:nth-child(3) > div.item-inner > div > ion-label > div > p"
segunda_button_selector = "body > ion-app > ng-component > ion-grid > ion-row > ion-col.menu-web.prueba-1.col > codere-sidebar-pc > div > ion-list.menuLatDestacados.list.list-md > ion-item:nth-child(4) > div.item-inner > div > ion-label > div > p"
nba_button_selector = "body > ion-app > ng-component > ion-grid > ion-row > ion-col.menu-web.prueba-1.col > codere-sidebar-pc > div > ion-list.menuLatDestacados.list.list-md > ion-item:nth-child(8) > div.item-inner > div > ion-label > div > p"
tennis_button_selector = "body > ion-app > ng-component > ion-grid > ion-row > ion-col.menu-web.prueba-1.col > codere-sidebar-pc > div > ion-list.menuLatDestacados.list.list-md > ion-item:nth-child(2) > div.item-inner > div > ion-label > div > p"

laliga_data = webscraping(url, laliga_button_selector)
print("LaLiga data:")
print(laliga_data)

segunda_data = webscraping(url, segunda_button_selector)
print("Segunda data:")
print(segunda_data)

nba_data = webscraping_nba(url, nba_button_selector)
print("NBA data:")
print(nba_data)

tennis_data = webscraping_tenis(url, tennis_button_selector, competition_selectors)
print("Tenis data:")
print(tennis_data)

headers = ["liga", "equipo1", "cuota1", "cuotaX", "cuota2", "equipo2"]

with open("codere.csv", "w") as codere_file:
    writer = csv.DictWriter(codere_file, fieldnames=headers)
    writer.writeheader()
    for partido in laliga_data:
        partido["liga"] = "LaLiga"
        writer.writerow(partido)
    for partido in segunda_data:
        partido["liga"] = "Segunda"
        writer.writerow(partido)
    for partido in nba_data:
        partido["liga"] = "NBA"
        writer.writerow(partido)
    for partido in tennis_data:
        partido["liga"] = "Tenis"
        writer.writerow(partido)
codere_file.close()
