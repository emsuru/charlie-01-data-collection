import requests
from bs4 import BeautifulSoup
import pandas as pd # I'm using pandas to save the URLs to a CSV file, as I'm familiar with this package
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures

# Function to handle the request and parsing for a single page
def get_links_from_page(base_url, page):
    search_url = f"{base_url}?countries=BE&page={page}"
    response = requests.get(search_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        property_links = soup.find_all('a', class_='card__title-link')
        return [link['href'] for link in property_links if 'href' in link.attrs]
    else:
        print(f"Failed to retrieve page {page}: {response.status_code}")
        return []

# This function retrieves the URLs of the properties listed on the Immoweb search results page
# It now uses concurrent requests to speed up the process
def get_property_links(base_url, pages):
    all_urls = []
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(get_links_from_page, base_url, page) for page in range(1, pages + 1)]
        for future in concurrent.futures.as_completed(futures):
            all_urls.extend(future.result())
    # urls_df = pd.DataFrame(all_urls, columns=['URL'])
    # urls_df.to_csv('property_urls.csv', index=False)
    return all_urls

# --- Code for testing purposes.

# base_search_url = 'https://www.immoweb.be/en/search/house-and-apartment/for-sale' # Define the base URL for the search results
# total_pages = 400

# # Specify the number of pages we want to scrape: (each search page contains 60 properties)
# 10 pages (600 unique URLS saved) takes 6 seconds
# 200 pages (12,000 unique URLs) taks 55 seconds
# 400 pages (24,000 unique URLs) takes 110 seconds

# --- Code for testing purposes.

# Get property URLs from the specified number of pages:
# property_urls = get_property_links(base_search_url, total_pages)
# print(len(property_urls)) # print the length of the list, to see how many page URLS we have
# print(property_urls[:10]) #print the first 10 urls, change this to print more if you want to see more
