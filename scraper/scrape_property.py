# Import necessary libraries
import requests  # Used to make HTTP requests
from bs4 import BeautifulSoup  # Used for parsing HTML and XML documents
import pandas as pd  # Data manipulation and analysis library
import json  # Library for JSON operations
import re  # Library for regular expression operations
import get_property_links  # Custom module to get property links (not used in this selection)

# Define the function to scrape property data.
def scrape_property(url):
    """
    Scrape property data from a list of URLs.

    This function requests each URL, parses the HTML content to extract property data,
    and then saves the data to a JSON and a CSV file.

    Args:
        urls (list): A list of URLs to scrape.

    Returns:
        dict: A dictionary containing the scraped data of the last property.
    """
    # Notify the user that the scraping process has begun
    print("Starting the scraping process for the provided URLs.")
    # Initialize a list to hold all property data
    all_property_data = []
    # Initialize a dictionary to hold data for the current property
    property_data = {}
    # Loop through each URL in the list of URLs
    for url in urls:
        # Print the URL that is currently being fetched
        print(f"Fetching data for URL: {url}")
        # Make an HTTP GET request to the URL
        response = requests.get(url)
        # Check if the request was successful (HTTP status code 200)
        if response.status_code == 200:
            # Notify the user of a successful data retrieval
            print(f"Successfully retrieved data for URL: {url}")
            # Parse the HTML content of the page using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            # Find all <script> tags in the HTML document
            scripts = soup.find_all('script')
            # Initialize variables to hold specific script contents
            data_layer_script = None
            av_items_script = None
            # Loop through each script tag found
            for script in scripts:
                # Check if the script contains the 'window.dataLayer' JavaScript object
                if 'window.dataLayer' in script.text:
                    # If found, store the script's text
                    data_layer_script = script.text
                # Check if the script contains the 'const av_items' JavaScript object
                if 'const av_items =' in script.text:
                    # If found, store the script's text
                    av_items_script = script.text

            # If the 'window.dataLayer' script was found
            if data_layer_script:
                # Find the start index of the JSON object within the script
                start = data_layer_script.find('window.dataLayer = [') + len('window.dataLayer = [')
                # Find the end index of the JSON object within the script
                end = data_layer_script.find('];', start)
                # If the end index is found
                if end != -1:
                    # Extract the JSON string from the script
                    json_str = data_layer_script[start:end]
                    # Remove any comments within the JSON string
                    json_str = re.sub(r'(?m)^\s*//.*\n?', '', json_str)
                    # Strip whitespace from the beginning and end of the JSON string
                    json_str = json_str.strip()
                    # Wrap the JSON string in square brackets to form a valid JSON array
                    json_str = '[' + json_str + ']'

                    # Print the JSON string before attempting to parse it
                    print("JSON string before parsing:", json_str)

                    # Attempt to parse the JSON string
                    try:
                        # Load the JSON string into a Python dictionary
                        data = json.loads(json_str)
                        # Extract the 'classified' object from the data
                        classified_data = data[0].get('classified', {})
                        # Extract various pieces of property data from the 'classified' object
                        bedroom_count = classified_data.get('bedroom', {}).get('count', '0')
                        kitchen_installed = 1 if classified_data.get('kitchen', {}).get('type', '') == 'installed' else 0

                        # Create a dictionary to hold the extracted property data
                        property_data = {
                            'id': classified_data.get('id', ''),
                            'type': classified_data.get('type', ''),
                            'subtype': classified_data.get('subtype', ''),
                            'price': classified_data.get('price', ''),
                            'zip': classified_data.get('zip', ''),
                            'constructionYear': classified_data.get('building', {}).get('constructionYear', ''),
                            'build_condition': classified_data.get('building', {}).get('condition', ''),
                            'bedroom_count': bedroom_count,
                            'kitchen_installed': kitchen_installed
                        }

                        # Notify the user of the extracted data for the current property
                        print(f"Extracted data for property ID: {property_data['id']}")

                        # If the 'const av_items' script was found
                        if av_items_script:
                            # Find the start and end indices of the JSON object within the script
                            start = av_items_script.find('const av_items =') + len('const av_items =')
                            end = av_items_script.find('}', start) + 1
                            # Extract the JSON string from the script
                            av_items_str = av_items_script[start:end]

                            # Load the JSON string into a Python dictionary
                            av_items_data = json.loads(av_items_str)
                            # Extract additional pieces of property data from the 'av_items' object
                            indoor_surface = av_items_data.get('indoor_surface', '')
                            building_state = av_items_data.get('building_state', '')
                            city = av_items_data.get('city', '')
                            province = av_items_data.get('province', '')
                            parking = '1' if av_items_data.get('parking', '') == 'true' else '0'
                            outdoor_terrace_exists = '1' if av_items_data.get('outdoor_terrace_exists', '') == 'true' else '0'
                            land_surface = av_items_data.get('land_surface', '')

                            # Update the property_data dictionary with the additional information
                            property_data.update({
                                'indoor_surface': indoor_surface,
                                'building_state': building_state,
                                'city': city,
                                'province': province,
                                'parking': parking,
                                'outdoor_terrace_exists': outdoor_terrace_exists,
                                'land_surface': land_surface
                            })

                            # Notify the user that additional information has been added to the property data
                            print(f"Updated property data with additional information for property ID: {property_data['id']}")

                    # If there is an error while parsing the JSON string
                    except json.JSONDecodeError as e:
                        # Print the error message
                        print(f"JSON parsing error: {e}")
                        # If the error object has a 'pos' attribute, print the part of the JSON string where the error occurred
                        error_pos = e.pos if hasattr(e, 'pos') else None
                        if error_pos:
                            print(json_str[max(error_pos - 50, 0):min(error_pos + 50, len(json_str))])
        # If the HTTP request was not successful
        else:
            # Notify the user that the data retrieval failed
            print(f"Failed to retrieve property data for URL: {url}, status code: {response.status_code}")
        # Add the current property's data to the list of all property data
        all_property_data.append(property_data)

    # Notify the user that the data is being written to files
    print("Writing the scraped data to the local JSON and CSV files.")

## Comment out these next 3 lines if you just want to call the function:
## and not save the data to a JSON file in here

    with open('data/property_data.json', 'w') as json_file:
        json.dump(all_property_data, json_file, indent=4)
        print("Data successfully written to property_data_test.json")

## Comment out these next 3 lines if you just want to call the function:
## and not save the data to a CSV file in here

    df = pd.DataFrame(all_property_data)  # Convert the dictionary to a pandas DataFrame first
    df.to_csv('data/property_data.csv', index=False)  #
    print("Data successfully written to property_data.csv")

    # Return the list of all property data
    return all_property_data

## --- These next 3 lines are execution code, comment out if calling from main.py

urls_df = pd.read_csv('input_data/property_urls_50.csv') # Read URLs from a CSV file into a pandas DataFrame
urls = urls_df.iloc[:, 0].tolist() # Convert the first column of the DataFrame to a list of URLs
scrape_property(urls) # Call the scrape_property function with the list of URLs

### ---- PLESE IGNORE EVERYTHING BELOW. THIS IS PART OF MY LEARNING PROCESS ----
## Instead of using a local CSV of already scraped URLs,
## this code would call a function that scrapes the URLs from the Immoweb website
## and then calls the scrape_property function with the list of URLs as an argument

# base_url = 'https://www.immoweb.be/en/search/house-and-apartment/for-sale'
# urls = get_property_links.get_property_links(base_url, 2)
# scrape_property(urls)

## This code externalises Save the data to a local JSON file and a local CSV file

# def write_to_csv(data, filename):
#     df = pd.DataFrame(data)
#     df.to_csv(filename, index=False)

# def write_to_json(data, filename):
#     with open(filename, 'w') as json_file:
#         json.dump(data, json_file, indent=4)

# A simple test for the scrape_property function:
# test_url = "https://www.immoweb.be/en/classified/apartment/for-sale/knokke-heist/8300/11156677"
# test_data = scrape_property(test_url)
# print("Test property data:", test_data)
