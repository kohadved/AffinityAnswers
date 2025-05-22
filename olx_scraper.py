import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import time
import random
import urllib.parse

def get_olx_listings(search_query):
    """
    Scrape car cover listings from OLX
    """
    # Encode the search query for URL
    encoded_query = urllib.parse.quote(search_query)
    search_url = f"https://www.olx.in/items/q-{encoded_query}"
    
    # Headers to mimic a browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Cache-Control': 'max-age=0'
    }
    
    try:
        print(f"Fetching data from: {search_url}")
        # Add a small delay to be respectful to the server
        time.sleep(random.uniform(2, 4))
        
        response = requests.get(search_url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Print response status and content type for debugging
        print(f"Response status: {response.status_code}")
        print(f"Content type: {response.headers.get('content-type', 'unknown')}")
        
        soup = BeautifulSoup(response.text, 'lxml')
        
        # Find all listing items
        listings = []
        items = soup.find_all('div', {'data-cy': 'l-card'})
        
        if not items:
            print("No listings found. This might be due to:")
            print("1. No items matching the search criteria")
            print("2. Website structure might have changed")
            print("3. Access might be blocked")
            print("\nTrying alternative selectors...")
            
            # Try alternative selectors
            items = soup.find_all('div', class_='_1AtVbE')
            if not items:
                items = soup.find_all('div', class_='css-1bbgabe')
        
        print(f"Found {len(items)} listings")
        
        for item in items:
            try:
                # Try different possible selectors for each field
                title_elem = item.find('h6') or item.find('div', class_='css-1bbgabe')
                price_elem = item.find('p', {'data-testid': 'ad-price'}) or item.find('span', class_='css-10b0gli')
                location_elem = item.find('p', {'data-testid': 'location-date'}) or item.find('span', class_='css-veheph')
                link_elem = item.find('a')
                
                if not all([title_elem, price_elem, location_elem, link_elem]):
                    continue
                
                title = title_elem.text.strip()
                price = price_elem.text.strip()
                location = location_elem.text.strip()
                link = 'https://www.olx.in' + link_elem['href'] if link_elem['href'].startswith('/') else link_elem['href']
                
                listing = {
                    'title': title,
                    'price': price,
                    'location': location,
                    'link': link
                }
                listings.append(listing)
                print(f"Successfully extracted listing: {title[:50]}...")
                
            except (AttributeError, KeyError) as e:
                print(f"Error extracting listing: {str(e)}")
                continue
        
        return listings
    
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        if hasattr(e.response, 'status_code'):
            print(f"Status code: {e.response.status_code}")
        if hasattr(e.response, 'text'):
            print("Response content preview:")
            print(e.response.text[:500])
        return []

def save_to_file(listings, filename):
    """
    Save the listings to a JSON file
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(listings, f, indent=4, ensure_ascii=False)
        print(f"\nSuccessfully saved {len(listings)} listings to {filename}")
    except IOError as e:
        print(f"Error saving to file: {e}")

def main():
    search_query = "car cover"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"olx_car_covers_{timestamp}.json"
    
    print("Starting OLX scraper...")
    listings = get_olx_listings(search_query)
    
    if listings:
        save_to_file(listings, output_file)
    else:
        print("\nNo listings were found. Please check the error messages above.")

if __name__ == "__main__":
    main() 