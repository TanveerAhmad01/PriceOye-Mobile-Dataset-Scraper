import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import time

class MobileScraper:
    def __init__(self, base_url, max_pages):
        self.base_url = base_url
        self.max_pages = max_pages
        self.title_list = []
        self.rating_list = []
        self.reviews_list = []
        self.discount_price_list = []
        self.original_price_list = []
        self.off_on_every_mobile_list = []
        self.discount_price = 0
        self.orignalPrice = 0
        self.header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
        }

    def scrape(self):
        for i in range(1, self.max_pages + 1):
            page_url = f'{self.base_url}?page={i}'
            response = requests.get(page_url, headers=self.header)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            main_content = soup.find('div', class_="product-list")
            content = main_content.find_all('div', 'productBox b-productBox')
            
            print(f"Scraping {len(content)} products from: {page_url}")
            
            for product in content:
                self.extract_product_data(product)

            time.sleep(3)

    def extract_product_data(self, product):
        # Title
        title = product.find('div', class_='p-title bold h5')
        self.title_list.append(title.text.strip() if title else None)
        
        # Rating
        rating = product.find('span', class_='h6 bold')
        getTitle = title.text.strip()
        print("Title: ",getTitle)
        self.rating_list.append(float(rating.text.strip()) if rating else None)
        
        # Reviews
        review = product.find('span', class_='rating-h7 bold')
        if review:
            number = review.text.split()[0]
            print("reviews: ",number)
            self.reviews_list.append(number if number else None)
        else:
            self.reviews_list.append(None)
        
        # Discount Price
        discount_price = product.find('div', class_='price-box p1')
        if discount_price: 
            number = discount_price.text.split()[1]
            removeComa = number.replace(',', '')
            self.discount_price = int(removeComa)
        else:
            self.discount_price = 0

        original_price = product.find('div', class_='price-diff-retail')
        if original_price:
            number = original_price.text.split()[1]
            orignal_nubmer = original_price.text.split()[1]
            removeComaorignal = orignal_nubmer.replace(',', '')
            self.orignalPrice = int(removeComaorignal)
        else:
            self.orignalPrice = 0
            
        
        if self.discount_price < self.orignalPrice:
            print("if conldition discounted price: ",self.discount_price,self.orignalPrice)
            self.original_price_list.append(self.orignalPrice if self.orignalPrice else None)
            self.discount_price_list.append(self.discount_price if self.discount_price else None)   
        else:
            print("else conldition discounted price: ",self.discount_price)
            self.original_price_list.append(self.discount_price if self.discount_price else None)
            self.discount_price_list.append(None)
        

        # Discount Percentage
        discount = product.find('div', class_='price-diff-saving')
        if discount:
            number = discount.text.split()[0]
            print("off price: ",number)
            self.off_on_every_mobile_list.append(number if number else None)
        else:
            self.off_on_every_mobile_list.append(None)

        print("---------------------------------------------------")

    def save_to_csv(self,filename='mobile_data.csv'):
        data= pd.DataFrame({
            'Title': self.title_list,
            'Rating': self.rating_list,
            'Reviews': self.reviews_list,
            'Discount Price': self.discount_price_list,
            'Original Price': self.original_price_list,
            'Off': self.off_on_every_mobile_list
        })
        
        data.to_csv(filename, index=False)
        print(f"\nData saved to {filename}")
        

base_url = 'https://priceoye.pk/mobiles'
max_pages = 23
obj = MobileScraper(base_url, max_pages)
obj.scrape()
obj.save_to_csv()
