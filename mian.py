import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}

base_url = 'https://priceoye.pk/mobiles'


counter = 1
maxRange = 23


titleList = []
ratingList = []
reviewsList = []
discountPriceList = []
originalPriceList = []
offOnEveryMobileList = []

for i in range(counter, maxRange + 1):
    pageUrl = f'{base_url}?page={i}'
    response = requests.get(pageUrl, headers=header)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    mainContent = soup.find('div', class_="product-list")
    content = mainContent.find_all('div', 'productBox b-productBox')
    
    print(f"Scraping {len(content)} products from: {pageUrl}")
    
    for product in content:
        # Title
        title = product.find('div', class_='p-title bold h5')
        titleList.append(title.text.strip() if title else None)
        
        # Rating
        rating = product.find('span', class_='h6 bold')
        ratingList.append(rating.text.strip() if rating else None)
        
        # Reviews
        review = product.find('span', class_='rating-h7 bold')
        if review:
            number = re.search(r'\d+', review.text) 
            reviewsList.append(number.group() if number else None)
        else:
            reviewsList.append(None)
        
        # Discount Price
        discountPrice = product.find('div', class_='price-box p1')
        if discountPrice:
            number = re.search(r'\d+', discountPrice.text)
            discountPriceList.append(number.group() if number else None)
        else:
            discountPriceList.append(None)
        
        # Original Price
        originalPrice = product.find('div', class_='price-diff-retail')
        if originalPrice:
            number = re.search(r'\d+', originalPrice.text)
            originalPriceList.append(number.group() if number else None)
        else:
            originalPriceList.append(None)
        
        # Discount Percentage
        discount = product.find('div', class_='price-diff-saving')
        if discount:
            number = re.search(r'\d+', discount.text)
            offOnEveryMobileList.append(number.group() if number else None)
        else:
            offOnEveryMobileList.append(None)


df = pd.DataFrame({
    'Title': titleList,
    'Rating': ratingList,
    'Reviews': reviewsList,
    'Discount Price': discountPriceList,
    'Original Price': originalPriceList,
    'Off': offOnEveryMobileList
})


print("\nScraped Data:")
print(df.head())


df.to_csv('mobiles_data.csv', index=False)
print("\nData saved to mobiles_data.csv")
