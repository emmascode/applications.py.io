from bs4 import BeautifulSoup
import requests
import pandas as pd

#scraping from multiple pages
#create a for loop

name = []
mileage = []
dealer_name = []
rating = []
rating_count = []
price = []

for i in range(1, 20):
    #website in a variable
    website = 'https://www.cars.com/shopping/results/?page=' + str(i) + '&page_size=20&error_state=false&list_price_max=&location_input_value=&location_type=&makes[]=mercedes_benz&maximum_distance=all&models[]=&stock_type=cpo&zip='
    #request to website
    response = requests.get(website)
    response.status_code
    #soup object    
    soup = BeautifulSoup(response.content,'html.parser')
    #results
    results = soup.find_all('div', {'class':'vehicle-card'})

    for result in results:
    #name
        try:
            name.append(result.find('h2').get_text())
        except:
            name.append('n/a')
        #mileage
        try:
            mileage.append(result.find('div', {'class': 'mileage'}).get_text()) 
        except:
            mileage.append('n/a')
        #dealer name
        try:
            dealer_name.append(result.find('div', {'class': 'dealer-name'}).get_text().strip()) 
        except:
            dealer_name.append('n/a')
        #rating
        try:
            rating.append(result.find('span', {'class': 'sds-rating__count'}).get_text()) 
        except:
            rating.append('n/a')
        #rating count
        try:
            rating_count.append(result.find('span', {'class': 'sds-rating__link'}).get_text())  
        except:
            rating_count.append('n/a')
        #price
        try:
            price.append(result.find('span', {'class': 'primary-price'}).get_text()) 
        except:
            price.append('n/a')

#create Pandas dataframe
car_dealer = pd.DataFrame({'Name': name, 'Mileage': mileage, 'Dealer Name': dealer_name,
                        'Rating': rating, 'Rating Count': rating_count, 'Price': price})

#data cleaning
car_dealer['Rating Count'] = car_dealer['Rating Count'].apply(lambda x: x.strip('review)').strip('('))
print(car_dealer)

#outut in excel
car_dealer.to_excel('multiple_pages_cars.xlsx', index=False)
