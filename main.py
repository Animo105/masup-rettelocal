from item import Item
from temp import getAllPages
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_NAME = "data.csv"

def getItems(driver, itemsArray) :
    try :
        for i in range(len(items)) :
            # Retourne le nom de l'item
            item_name = itemsArray[i].find_element(By.CSS_SELECTOR, "h3[data-testid='product-title']").text

            try :
                item_company = itemsArray[i].find_element(By.CSS_SELECTOR, "p[data-testid='product-brand']").text
            except :
                item_company = ""
            
            item_p_to_w = itemsArray[i].find_element(By.CSS_SELECTOR, "p[data-testid='product-package-size'").text

            item_pt = driver.find_element(By.CSS_SELECTOR, "h1[data-testid='heading']").text


            item_im_li = itemsArray[i].find_element(By.TAG_NAME, "img").get_attribute("src")

            # Retourne l'élément contenant les informations sur le prix du produit
            temp_price_tiles = itemsArray[i].find_element(By.CSS_SELECTOR, "div[data-testid='price-product-tile']").find_elements(By.XPATH, "./*")
            # Trouve le prix de l'item et ajuste le contenu du String retourné pour donner un float
            item_price = ""
            # Si le div qui contient le prix n'a qu'un élément enfant
            if len(temp_price_tiles) == 1 :
                # On va chercher directement le contenu de l'élément
                item_price = temp_price_tiles[0].text
            else :
                try :
                    # On va chercher le contenu du premier élément, qui aura alors d'autres éléments à l'intérieur
                    item_price = (temp_price_tiles[0].find_element(By.CSS_SELECTOR, "span[data-testid='sale-price']").text)
                except :
                    item_price = (temp_price_tiles[0].find_element(By.CSS_SELECTOR, "span[data-testid='regular-price']").text)
            # On enlève la mention du mot 'environ' (lorsque l'item est vendu au poid) et le signe '$'
            # On transforme 'item_price' en float pour pouvoir le mettre dans le constructeur de la classe 'Item'
            item_price = item_price.replace("sale","").replace("environ", "").replace("$", "").replace(",", ".").strip()
            item_price = float(item_price[:4])

            # Ajoute les informations récupérés à partir du site web dans la liste des items
            temp_item_list.append(Item(na=item_name, co=item_company, pw=item_p_to_w, li=item_im_li, pt=item_pt, pr=item_price))

            # Affiche l'item créé
            print("Item no " + str(len(temp_item_list)) + "\n" + str(temp_item_list[len(temp_item_list) - 1]))
    except :
        print("Error while reading element. Reloading...")
        sleep(1)
        temp_item_list.clear()
    finally :
        return temp_item_list

#######################################################################
###                            MAIN CODE                            ###
#######################################################################
path = os.path.join(SCRIPT_DIR, FILE_NAME)

if os.path.exists(path):
    os.remove(path)

with open(path, 'w') as f:
    f.write("Name; company; price; price_to_weight; product_type; image_link\n")

item_list = list()

driver = webdriver.Firefox()

page_list = getAllPages(driver)
print(len(page_list))

for k in page_list :
    driver.get(k)
    nb_pages = 0
    try :
        nb_pages = driver.find_element(By.CSS_SELECTOR, "div[data-testid='pagination']").find_elements(By.TAG_NAME, "a")
        nb_pages = int(nb_pages[len(nb_pages) - 2].text)
    except :
        nb_pages = 1
    print(nb_pages)

    for y in range(nb_pages) :
        temp_item_list = list()
        
        items_section = driver.find_elements(By.CSS_SELECTOR, "div[data-testid='product-grid-component']")
        items = items_section[1].find_elements(By.CSS_SELECTOR, ".chakra-linkbox.css-yxqevf")
        
        is_loaded = False

        while is_loaded == False :
            try :
                temp_item_list = getItems(driver, items)
                is_loaded = True
            except :
                try :
                    print("Bad item request. Reloading...")
                    items_section = driver.find_elements(By.CSS_SELECTOR, "div[data-testid='product-grid-component']")
                    items = items_section[1].find_elements(By.CSS_SELECTOR, ".chakra-linkbox.css-yxqevf")
                except :
                    pass

        for i in temp_item_list :
            item_list.append(i)

        with open(path, 'a', encoding="utf-8") as f:
            for i in temp_item_list:
                if isinstance(i, Item):
                    try:
                        f.write(f"{i.name};{i.company};{i.price};{i.price_to_weight};{i.product_type};{i.image_link}\n")
                    except Exception as e:
                        print("Error while writing item: ", i.name)
                        print(e, "\n")

        if (y < nb_pages - 1) :
            # Ouvre vert la prochaine page
            try :
                driver.find_element(By.CSS_SELECTOR, "#onetrust-accept-btn-handler").click()
                sleep(2)
            except :
                pass
            driver.find_element(By.CSS_SELECTOR, "a[aria-label='Page suivante']").click()
            sleep(5)

print(len(item_list))
driver.quit()