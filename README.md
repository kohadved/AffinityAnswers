# OLX Car Cover Scraper

This Python script scrapes car cover listings from OLX India and saves them to a JSON file.

## Features

- Scrapes car cover listings from OLX India
- Extracts title, price, location, and link for each listing
- Saves results to a timestamped JSON file
- Includes error handling and rate limiting
- Respects website's resources with random delays

## Requirements

- Python 3.6 or higher
- Required packages listed in `requirements.txt`

## Installation

1. Clone this repository:
```bash
git clone <your-repo-url>
cd <repo-directory>
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

Simply run the script:
```bash
python olx_scraper.py
```

The script will:
1. Fetch car cover listings from OLX
2. Save the results to a JSON file named `olx_car_covers_YYYYMMDD_HHMMSS.json`
3. Print status messages to the console

## Output Format

The script generates a JSON file with the following structure:
```json
[
    {
        "title": "Car Cover Title",
        "price": "₹ Price",
        "location": "Location and Date",
        "link": "https://www.olx.in/item-url"
    },
    ...
]
```

## Notes

- The script includes a random delay between requests to be respectful to OLX's servers
- Make sure you have a stable internet connection
- The script uses a user agent to mimic a browser request
- Some listings might be skipped if they have missing data

## Disclaimer

This script is for educational purposes only. Please respect OLX's terms of service and robots.txt when using this scraper. Excessive scraping might get your IP blocked. 