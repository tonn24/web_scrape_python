from bs4 import BeautifulSoup
import requests

import json

start_url = 'https://www.hinnavaatlus.ee/products/Tahvelarvutid/Tahvelarvutid/?sort=-views'

def empty_data_file():
    f = open('data.json', 'r+')
    f.truncate(0)
    f.close()

def parse(start_urls):
    
    page = requests.get(start_urls)
    soup = BeautifulSoup(page.text, 'html.parser')
    
    tablet_list = soup.find_all("li", class_ = 'product-list-item')
    
    for item in tablet_list:
        
        data = {'Title': '', 'Price': '', 'Picture href': '',}
        data['Title'] = item.h3.get_text().strip() if item.h3 != None else ''
        
        
        raw_price_element = item.find(class_= "product-list-price-line clear")
        
        if(raw_price_element != None):
            encoded = raw_price_element.get_text().strip().encode("ascii", "ignore")
            price_element = encoded.decode()
        else:
            price_element = ''
            
        data['Price'] = price_element[0:-7]
        
        
        data['Picture href'] = item.img['src']

        
        try:
            with open('data.json', 'a') as fp:
                
                json.dump(data, fp, indent = 2)
            fp.close()
    
           
        except:
            print("Error!")
                
        
    try:
        link = soup.find('a', class_ = 'page').get('href')
        link = soup.find('li', class_ = 'pagination-item item pagination-next').a['href']
        next_page = 'https://www.hinnavaatlus.ee/' + link
        if next_page:

            print(next_page)
            parse(next_page)
    except:
          print("No more pages")
    
            
if __name__ == '__main__':
    empty_data_file()
    parse(start_url)


