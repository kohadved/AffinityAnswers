import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import time
import random

def get_olx_listings(search_url):
    """
    Scrape car cover listings from OLX
    """
    # Headers to mimic a browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        # Add a small delay to be respectful to the server
        time.sleep(random.uniform(1, 3))
        
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        soup = BeautifulSoup(response.text, 'lxml')
        
        # Find all listing items
        listings = []
        items = soup.find_all('div', {'data-cy': 'l-card'})
        
        for item in items:
            try:
                title = item.find('h6').text.strip()
                price = item.find('p', {'data-testid': 'ad-price'}).text.strip()
                location = item.find('p', {'data-testid': 'location-date'}).text.strip()
                link = 'https://www.olx.in' + item.find('a')['href']
                
                listing = {
                    'title': title,
                    'price': price,
                    'location': location,
                    'link': link
                }
                listings.append(listing)
            except AttributeError:
                continue  # Skip items with missing data
        
        return listings
    
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return []

def save_to_file(listings, filename):
    """
    Save the listings to a JSON file
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(listings, f, indent=4, ensure_ascii=False)
        print(f"Successfully saved {len(listings)} listings to {filename}")
    except IOError as e:
        print(f"Error saving to file: {e}")

def main():
    search_url = "https://www.olx.in/items/q-car-cover"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"olx_car_covers_{timestamp}.json"
    
    print("Starting OLX scraper...")
    listings = get_olx_listings(search_url)
    
    if listings:
        save_to_file(listings, output_file)
    else:
        print("No listings found or an error occurred.")

if __name__ == "__main__":
    main() 