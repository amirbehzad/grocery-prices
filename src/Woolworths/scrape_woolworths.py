'''

    Scrape product data from Woolworths.com.au using Selenium

    If you run this file it will scrape a sample of products - one page per category.

    We use several Javascript files. The Javascript is injected into a web page, extracts data and returns it as a JSON
    encoded string. Data is saved to the 'src/Datasets' folder as a JSON file with the name of the category.

    You can use get_all_categories() to get the names of categories which you can then scrape with scrape_products()

    It takes exponentially longer to retrieve nutritional information or product images because each of these require an
    extra web request for every single product. We do not currently use nutritional info or images in our analysis.


'''

import json, requests, time, random

# Web scraping library
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

browser = webdriver.Chrome()
base_url = 'https://www.woolworths.com.au/shop/browse/'

def execute_script(filename):
    '''' Injects Javascript into the browser and returns JSON
    :param filename: the name of the file containing Javascript to inject
    :return: JSON data - can be either a list or dictionary '''
    f = open(filename, 'r')
    json_string = browser.execute_script(f.read())
    f.close()
    json_data = json.loads(json_string)
    return json_data

def save_json(filename, data):
    ''' Saves data as a JSON file named filename
    :param filename: the name of the file to save
    :param data: a dictionary that will be encoded as a JSON string '''
    f = open(filename, 'w+')
    json_string = json.dumps(data, indent=4, sort_keys=True)
    f.write(json_string)
    f.close()

def get_all_categories():
    ''' Returns a list of all top level / main product categories for Woolworths.com.au
    :return: list of all categories '''
    browser.get('https://www.woolworths.com.au')
    categories = execute_script('scrape_categories.js')
    return categories

def scrape_all_products(get_nutrition_info = False, save_images = False, max_num_pages=float('inf')):
    ''' Scrape all products for all categories
    :param max_num_pages: the maximum number of pages to scrape for each category
    :param get_nutrition_info: boolean - scrape product nutrition info, requires an extra web request for every product
    :param save_images: boolean - scrape images of products, requires an extra web request for every product '''
    all_categories = get_all_categories()
    scrape_products(all_categories, get_nutrition_info, save_images, max_num_pages)

def scrape_products(categories, get_nutrition_info = False, save_images = False, max_num_pages = float('inf')):
    ''' Scrape data for all products under the categories provided and save as JSON file
    :param categories: the categories to scrape products for
    :param get_nutrition_info: boolean - scrape product nutrition info, requires an extra web request for every product
    :param save_images: boolean - scrape images of products, requires an extra web request for every product
    :param max_num_pages: the maximum number of pages to scrape for each category
    :return: none '''

    # a dictionary of categories
    # the keys are category names
    # the values are the accumulated JSON for all products in that category
    data = {}

    items = set() # use a set of item names to avoid duplicates

    # Loop through all categories
    for category in categories:

        page_number = 1

        # Construct URL for first page in category
        url = base_url + category + '?pageNumber=' + str(page_number)

        data[category] = [] # JSON for all products in this category

        # Loop through all pages in this category
        while url != 'NONE':

            # Break if we have scraped the maximum desired number of pages for this category
            if page_number > max_num_pages:
                break

            # Get the next page
            browser.get(url)

            # Selenium only waits for the HTML DOM to load.
            # We are scraping dynamically loaded content so we have to explicitly make Selenium wait until this is loaded
            # Wait until the presence of a HTML element with the class 'paging-next' is detected
            try:
                timeout = 10
                WebDriverWait(browser, timeout).until(EC.presence_of_element_located((By.CLASS_NAME, 'paging-next')))
            except TimeoutException: # last page of category
                pass

            # Inject javascript to harvest data for all products on this page
            page_data = execute_script('scrape_products.js')

            # Get nutrition info / product images
            # we didn't use these in our analysis - safe to ignore
            if save_images or get_nutrition_info:

                for product in page_data['products']:

                    # Get product image
                    if save_images:
                        f = open(product['imgName'], 'wb')
                        image = requests.get(product['imgSrc']).content
                        f.write(image)
                        f.close()
                        time.sleep(random.randint(1,5))

                    # Get nutrition information
                    if get_nutrition_info:
                        browser.get(product['href'])
                        product['nutrition'] = execute_script('scrape_nutrition.js')['nutrition']
                        time.sleep(random.randint(1,5))

            # Add all products on this page to accumulated JSON for this category
            for product in page_data['products']:
                if product['name'] not in items: # avoid duplicates
                    items.add(product['name'])
                    product['category'] = category # add category to product JSON
                    data[category].append(product) # add product JSON to accumulated JSON for this category


            # Iterate loop
            url = page_data['nextPage']
            page_number += 1
            time.sleep(random.randint(1,5))

        # Save data for this category
        # (subcategories may contain slashes - which we replace have to with hyphens for the filename)
        filename = '../Datasets/Woolworths/' + category.replace('/', '-') + '.json'
        save_json(filename, data[category])

if __name__ == '__main__':
    scrape_all_products()
