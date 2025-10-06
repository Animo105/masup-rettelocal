from selenium.webdriver.common.by import By
from selenium import webdriver
from time import sleep



def getAllPages(driver) -> list :
    pages = list()
    driver.get("https://www.maxi.ca/fr")
    driver.set_window_size(1280, 720)
    sleep(5)
    try :
        driver.find_element(By.CSS_SELECTOR, "#onetrust-accept-btn-handler").click()
        sleep(2)
    except :
        pass
    menu = driver.find_element(By.CSS_SELECTOR, "ul[class='flex flex-row items-center justify-start']")
    menu = menu.find_element(By.TAG_NAME, "li")
    menu.click()
    all_buttons = driver.find_element(By.CSS_SELECTOR, "div[data-testid='iceberg-main-nav-l2-tabs-list']").find_elements(By.TAG_NAME, "button")

    for i in all_buttons :
        i.click()
        current_content = driver.find_element(By.CSS_SELECTOR, "ul[data-testid='iceberg-main-nav-l3-content-list']")
        all_pages = current_content.find_elements(By.TAG_NAME, "a")
        for y in all_pages :
            is_bold = False
            for s in y.get_attribute("class").split(" ") :
                if s == "font-bold" :
                    is_bold = True
            if not is_bold :
                pages.append(y.get_attribute("href"))
    return pages

