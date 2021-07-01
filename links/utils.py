import requests 
import lxml
from bs4 import BeautifulSoup

def get_price(url):
    
    def trimmer(x):
        if len(x) == 11:
            x = x[0] + x[2:4] + x[5:11]
            return float(x)         
        elif len(x) == 9:
            x = x[0:2] + x[3:]
            return float(x)
        elif len(x) > 6:
            x = x[0] + x[2:]
            return float(x) 
        
        return float(x)
    
    #Scraping variables
    headers = {
    'User-Agent':'https://developers.whatismybrowser.com/useragents/parse/?analyse-my-user-agent=yes',
    'Accept-Language': 'en',
    }

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    # print(soup.prettify())

    # getText will give only the content inside the span id and strip will remove white spaces 
    name = soup.select_one(selector = '#productTitle').getText().strip()
    # print(name)

    mrp = soup.select_one(selector = '.priceBlockStrikePriceString').getText().strip()[2:]
    mrp = trimmer(mrp)
        
    # print(mrp)

    #one of the two will hold the current price 
    current_price_1 = soup.select_one(selector = '#priceblock_dealprice')
    current_price_2 = soup.select_one(selector = '#priceblock_ourprice')

    if current_price_1 == None:
        current_price = current_price_2.getText().strip()[2:]
        
    if current_price_2 == None:
        current_price = current_price_1.getText().strip()[2:]

    if current_price_1 == None and current_price_2 == None:
        current_price = 'No Current Price available'

    #print(current_price)
    current_price = trimmer(current_price)
    
    save = soup.select_one(selector='.priceBlockSavingsString')

    if save == None:
        save = 'Not Available'
    else:
        save = save.getText().strip()
        
    # print(save)
    
    # for Image
    img = soup.select_one('#landingImage')
    img = img['src']
    img_link = requests.get(img) 


    # f = open(f'media/items/{name_for_title}.jpg', 'wb') 
    # f.write(img_link.content)
    # f.close()

    return name, current_price, mrp, save, img

# print(get_price('https://www.amazon.in/gp/product/B0764HS2X4/ref=ox_sc_saved_image_2?smid=A14CZOWI0VEHLG&psc=1'))