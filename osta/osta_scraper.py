from bs4 import BeautifulSoup
import requests

import json

start_url = 'https://www.osta.ee/kategooria/arvutid/lauaarvutid'

def empty_data_file():
    f = open('data.json', 'r+')
    f.truncate(0)
    f.close()

def parse(start_urls):

    page = requests.get(start_urls)
    soup = BeautifulSoup(page.text, 'html.parser')
    
    computer_list = soup.find_all("li", class_ = 'col-md-4 mb-30')

    for item in computer_list:
        
        data = {'Title': '', 'Price': '', 'Picture href': '',}
        data['Title'] = item.h3.get_text().strip()
        
        raw_price = item.find(class_= "offer-thumb__price--current")
        stripped_price = raw_price.get_text().strip()
        data['Price'] = stripped_price
        
        data['Picture href'] = item.a['style'][23:-3]
        
        
        try:
            
            with open('data.json', 'a') as fp:
                
                json.dump(data, fp, indent = 2)
            fp.close()
    
           
        except:
            print("Error!")
                
        
    try:
        
        link = soup.find('a', class_ = 'icon next page-link').get('href')
        print(link)
        next_page = 'https://www.osta.ee/' + link
        if next_page:
            print(next_page)
            parse(next_page)
    except:
          print("No more pages")
    
            
if __name__ == '__main__':
    empty_data_file()
    parse(start_url)


