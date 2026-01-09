import pandas, selenium
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium_stealth import stealth
import time

#search = input("По какому запросу искать товары? ")
def Search(search_query):
    search = search_query
    url = f"https://www.wildberries.ru/catalog/0/search.aspx?search={search}"
    return url



def init_webdriver(): #создаем webdriver для того что бы эмулировать работу пользователя
    driver = webdriver.Chrome()
    stealth(driver,
    languages=["en-US", "en"],
    vendor="Google Inc.", 
    platform="Win32",
    webgl_vendor="Intel Inc.",
    renderer="Intel Iris OpenGL Engine",
    fix_hairline=True,
    run_on_insecure_origins=False)
    return driver



def scrolldown(driver, deep): #прокручиваем страницу вниз что бы прогрузить страницу
    for _ in range(deep):
        driver.execute_script('window.scrollBy(0, 500)')
        time.sleep(0.1) 



    
def get_page(url): #запускаем вебдрайвер и прогружааем
    driver = init_webdriver()
    driver.get(url)
    time.sleep(5)
    scrolldown(driver, 40)
    html = driver.page_source
    driver.quit()
    return html


def parser(url):
    product_pack = []
    html = get_page(url)
    data = BeautifulSoup(html, "lxml")
    product = data.find_all("article", class_="product-card j-card-item j-analitics-item")
    
    for _ in product:
        title = _.find("span", class_="product-card__name").text.strip()[2:] #убираем первые два символа в виде " \"

    
        price_elem = _.find("ins", class_="price__lower-price wallet-price red-price")
        if price_elem:
            price = price_elem.text.strip()
        else:
            price_elem = _.find("ins", class_="price__lower-price wallet-price") 
            if price_elem:
                price = price_elem.text.strip()

        brand_span = _.h2.find("span", class_ = "product-card__brand")
        if brand_span:
            brand = brand_span.text.strip()
        else:
            brand = "Нету бренда"
        
        rate_span = _.div.find("span", class_ = "address-rate-mini address-rate-mini--sm")
        if rate_span:
            rate = rate_span.text.strip()
        else:
            rate = "Нет отзывов"

        data_span = _.div.find("span", class_ = "btn-text")
        if data_span:
            data = data_span.text.strip()
        else:
            data = "На случай непридведенных обстоятельств" #в случае если не будет по какой то причине нужного формата

        link = _.a.get("href")
        
        product_pack.append({
            "title": title,
            "price": price,
            "link": link,
            "brand": brand,
            "rate": rate,
            "data": data
        })
    return product_pack

    

