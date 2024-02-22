import requests
from bs4 import BeautifulSoup
# pandas is imported but not used in the current selection, it's intended for saving data to CSV
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures

def get_links_from_page(base_url, page):
    """
    Makes a GET request to a given URL to retrieve property links from a single page.

    Args:
        base_url (str): The base URL of the property listing site.
        page (int): The page number to retrieve the links from.

    Returns:
        list: A list of URLs found on the page. If the page fails to load, returns an empty list.
    """
    # Construct the search URL by appending the page number to the base URL
    search_url = f"{base_url}?countries=BE&page={page}"
    # Make the GET request to the search URL
    response = requests.get(search_url)
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the content of the page using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        # Find all the 'a' tags with class 'card__title-link' which contain the property links
        property_links = soup.find_all('a', class_='card__title-link')
        # Extract the 'href' attribute from each link tag to get the URL
        return [link['href'] for link in property_links if 'href' in link.attrs]
    else:
        # If the page fails to load, print an error message with the status code
        print(f"Failed to retrieve page {page}: {response.status_code}")
        return []

def get_property_links(base_url, pages):
    """
    Retrieves property links from multiple pages using concurrent requests.

    Args:
        base_url (str): The base URL of the property listing site.
        pages (int): The total number of pages to scrape.

    Returns:
        list: A list of all property URLs retrieved from the specified number of pages.
    """
    # Initialize an empty list to store all URLs
    all_urls = []
    # Use ThreadPoolExecutor to execute requests in parallel
    with ThreadPoolExecutor() as executor:
        # Create a future for each page request
        futures = [executor.submit(get_links_from_page, base_url, page) for page in range(1, pages + 1)]
        # As each future completes, extend the all_urls list with the results
        for future in concurrent.futures.as_completed(futures):
            all_urls.extend(future.result())
    # Uncomment the following lines if you want to save the URLs to a CSV file
    # urls_df = pd.DataFrame(all_urls, columns=['URL'])
    # urls_df.to_csv('property_urls.csv', index=False)
    return all_urls

# --- IGNORE EVERYTHING BELOW. PART OF MY LEARNING PROCESS. ----
# Code for testing purposes.

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
