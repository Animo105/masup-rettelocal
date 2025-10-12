from selenium.webdriver.common.by import By
from selenium import webdriver
from time import sleep



def getAllPages(driver) -> list :
    pages = list()
    driver.get("https://www.superc.ca/fr")
    driver.set_window_size(1280, 720)
    sleep(2)
    try :
        driver.find_element(By.CSS_SELECTOR, "#onetrust-reject-all-handler").click()
        sleep(2)
    except :
        pass
    driver.find_element(By.CSS_SELECTOR, "#navigation-level1--aisles").click()
    menu = driver.find_element(By.CSS_SELECTOR, "div[class='sub--nav--first']").find_element(By.TAG_NAME, "ul")
    all_li = menu.find_elements(By.CSS_SELECTOR, "li")
    sleep(2)

    all_li[0].find_element(By.CSS_SELECTOR, "button").click()
    sleep(1)
    for i in all_li :
        i.find_element(By.CSS_SELECTOR, "button").click()
        sleep(0.2)
        pages.append(driver.find_element(By.CSS_SELECTOR, ".aisles--subNav--lev2").find_element(By.TAG_NAME, "a").get_attribute("href"))
    return pages