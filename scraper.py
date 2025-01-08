from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import pandas as pd
chromedriver_path = r"D:\chromedriver-win64\chromedriver-win64\chromedriver.exe"
service = Service(chromedriver_path)

# Add Chrome options to ignore SSL errors
chrome_options = Options()
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--disable-web-security")
chrome_options.add_argument("--allow-running-insecure-content")

driver = webdriver.Chrome(service=service, options=chrome_options)
#This is the link that we are scraping the data from
url="https://www.nike.com/w/sale-shoes-3yaepzy7ok"

driver.get(url)

#Logic for Infinite Scrolling page, This code scrolls whole page first to load all the HTML from which data is scraped at later point.
last_height=driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    time.sleep(2)
    new_height=driver.execute_script('return document.body.scrollHeight')
    if new_height==last_height:
        break
    last_height=new_height

#Data Scraping using Beautiful Soup
soup=BeautifulSoup(driver.page_source,'lxml')
product_card=soup.find_all('div', class_= 'product-card__body')
df = pd.DataFrame(columns=['Link', 'Name', 'Subtitle', 'Price', 'Sale Price'])
for product in product_card:
    try:
        link=product.find('a',class_='product-card__link-overlay').get("href")
        name=product.find('div',class_='product-card__title').text
        subtitle=product.find('div',class_='product-card__subtitle').text
        full_price=product.find('div',class_='product-price us__styling is--striked-out css-0').text
        sale_price=product.find('div',class_='product-price is--current-price css-1ydfahe').text
        df.loc[len(df)] = {
            'Link': link,
            'Name': name,
            'Subtitle': subtitle,
            'Price': full_price,
            'Sale Price': sale_price
        }
    except:
        pass
    

#Saving the scraped data to .csv file   
print(df.head(10))
df.to_csv('nike_shoe_sale_data.csv', index=False) 
input("Press Enter to close...")
driver.quit()
