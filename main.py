from scraper import get_property_links, scrape_property
from scraper.save_data import write_to_csv, write_to_json
import pandas as pd

def main():
    base_search_url = 'https://www.immoweb.be/en/search/house-and-apartment/for-sale'
    pages = 400 # change / update this number before executing the program (the bigger this number, the longer it will take to run)

    property_urls = get_property_links(base_url=base_search_url, pages=pages)

    properties_data = [scrape_property(url) for url in property_urls]

    write_to_json(data=properties_data, filename='properties_data.json')     # Save to JSON
    write_to_csv(data=properties_data, filename='properties_data.csv')       # Save to CSV

if __name__ == "__main__":
    main()
