import pandas as pd

# for running selenium
from time import sleep
import selenium
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

def find_nearest_bank_of_america(df):
    """This function pulls in data from a csv and returns a dataframe with the additional columns of address
    and distance of the closest bank locations"""
    rank_list = []
    location_name = []
    bank_location_address = []
    bank_location_name = []
    distance_to_bank = []

    text = 'This Financial Center has been temporarily closed. Please visit one of our neighboring ATMs or utilize Online and Mobile Banking, all of which are available 24 hours a day, 7 days a week.  To make an appointment to access your safe deposit box during regular business hours, email us your full name, address and phone number at:safebox@bofa.com .'

    
    browser = webdriver.Chrome(ChromeDriverManager().install())
    sleep(1)


    for i in df.index: 
        
        # get url from dataframe
        url = f'https://locators.bankofamerica.com/?lat={df.Latitude[i]}&lng={df.Longitude[i]}'
    
        # let selenium do its magic
        
        browser.get(url)
        sleep(2)
        location = browser.find_elements_by_class_name("map-list-item")

        # debugging
        print(i)

        #number of inputs returned: this returns top five closest locations, unless it has less than 5 locations then it returns that number of locations.
        if len(location) >= 5:
            z = 5
        else:
            z = len(location)
        
        #build out lists of responses from webscrape
        for x in range(z):
            if location[x].text.split('\n')[6] == text:
                continue
                
            else:
                
                location_id = df.location_id[i]
                address = location[x].text.split('\n')[5]
                distance = location[x].text.split('\n')[3]
                name = location[x].text.split('\n')[1]

                # create lists from data
                rank_list.append(x)
                location_name.append(location_id)
                bank_location_name.append(name)
                bank_location_address.append(address)
                distance_to_bank.append(distance)
        
    
    return df, rank_list, location_name, bank_location_name, bank_location_address, distance_to_bank


def create_bank_df(location_name, rank_list, bank_location_name, bank_location_address, distance_to_bank):
    """This function takes in a series of lists and turns them into a data frame.  
    Then pivots the data frame by location id to return a usable df for locating nearest banks"""
    
  
    data = {'location_id': location_name,
           'distance_rank': rank_list,
            f'name_of_bank_location': bank_location_name, 
            f'address_of_bank': bank_location_address, 
            f'distance_to_bank': distance_to_bank}
    
    locations = pd.DataFrame(data)
    
    locations['for_operators'] = (locations.name_of_bank_location +
                              " Bank of America Location is at " +
                              locations.address_of_bank +
                              ".  This is " +
                              locations.distance_to_bank +
                              " miles from your retail location"
                             )
    
    
    for_export = locations.pivot(index='location_id', columns='distance_rank', values='for_operators').fillna('location closed')
    
    return for_export
