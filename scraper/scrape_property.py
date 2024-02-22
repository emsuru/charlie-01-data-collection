import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import re
import get_property_links
import pandas as pd

def scrape_property(urls):
    """
    Scrape property data from a list of URLs.

    This function requests each URL, parses the HTML content to extract property data,
    and then saves the data to a JSON and a CSV file.

    Args:
        urls (list): A list of URLs to scrape.

    Returns:
        dict: A dictionary containing the scraped data of the last property.
    """
    print("Starting the scraping process for the provided URLs.")
    property_data = {}
    for url in urls:
        print(f"Fetching data for URL: {url}")
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Successfully retrieved data for URL: {url}")
            soup = BeautifulSoup(response.content, 'html.parser')
            scripts = soup.find_all('script')
            data_layer_script = None
            av_items_script = None
            for script in scripts:
                if 'window.dataLayer' in script.text:
                    data_layer_script = script.text
                if 'const av_items =' in script.text:
                    av_items_script = script.text

            if data_layer_script:
                start = data_layer_script.find('window.dataLayer = [') + len('window.dataLayer = [')
                # Find the correct end of the JSON array
                end = data_layer_script.find('];', start)
                if end != -1:
                    json_str = data_layer_script[start:end]
                    json_str = re.sub(r'(?m)^\s*//.*\n?', '', json_str)
                    json_str = json_str.strip()
                    json_str = '[' + json_str + ']'

                    print("JSON string before parsing:", json_str)

                    try:
                        data = json.loads(json_str)
                        classified_data = data[0].get('classified', {})
                        bedroom_count = classified_data.get('bedroom', {}).get('count', '0')
                        kitchen_installed = 1 if classified_data.get('kitchen', {}).get('type', '') == 'installed' else 0

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

                        print(f"Extracted data for property ID: {property_data['id']}")

                        if av_items_script:
                            start = av_items_script.find('const av_items =') + len('const av_items =')
                            end = av_items_script.find('}', start) + 1
                            av_items_str = av_items_script[start:end]

                            av_items_data = json.loads(av_items_str)
                            indoor_surface = av_items_data.get('indoor_surface', '')
                            building_state = av_items_data.get('building_state', '')
                            city = av_items_data.get('city', '')
                            province = av_items_data.get('province', '')
                            parking = '1' if av_items_data.get('parking', '') == 'true' else '0'
                            outdoor_terrace_exists = '1' if av_items_data.get('outdoor_terrace_exists', '') == 'true' else '0'
                            land_surface = av_items_data.get('land_surface', '')

                            property_data.update({
                                'indoor_surface': indoor_surface,
                                'building_state': building_state,
                                'city': city,
                                'province': province,
                                'parking': parking,
                                'outdoor_terrace_exists': outdoor_terrace_exists,
                                'land_surface': land_surface
                            })

                            print(f"Updated property data with additional information for property ID: {property_data['id']}")

                    except json.JSONDecodeError as e:
                        print(f"JSON parsing error: {e}")
                        error_pos = e.pos if hasattr(e, 'pos') else None
                        if error_pos:
                            print(json_str[max(error_pos - 50, 0):min(error_pos + 50, len(json_str))])
        else:
            print(f"Failed to retrieve property data for URL: {url}, status code: {response.status_code}")

    print("Writing the scraped data to the local JSON and CSV files.")
    with open('property_data_test.json', 'w') as json_file:
        json.dump(property_data, json_file, indent=4)
        print("Data successfully written to property_data_test.json")

    df = pd.DataFrame([property_data])  # Convert the dictionary to a pandas DataFrame first
    df.to_csv('property_data_test.csv', index=False)  # Save the data to a local CSV file
    print("Data successfully written to property_data_test.csv")

    return property_data


urls_df = pd.read_csv('data/property_urls_6k.csv')
urls = urls_df.iloc[:, 0].tolist()
scrape_property(urls)

# --- Comment this
# base_url = 'https://www.immoweb.be/en/search/house-and-apartment/for-sale'
# urls = get_property_links.get_property_links(base_url, 2)
# scrape_property(urls)

##Save the data to a local JSON file and a local CSV file

# def write_to_csv(data, filename):
#     df = pd.DataFrame(data)
#     df.to_csv(filename, index=False)

# def write_to_json(data, filename):
#     with open(filename, 'w') as json_file:
#         json.dump(data, json_file, indent=4)
# Simple test for the scrape_property function
# test_url = "https://www.immoweb.be/en/classified/apartment/for-sale/knokke-heist/8300/11156677"
# test_data = scrape_property(test_url)
# print("Test property data:", test_data)
# No longer necesssary. Save the data to a local JSON file
# with open('property_data.json', 'w') as json_file:
#     json.dump(test_data, json_file, indent=4)
