'''

    Scrape product data from Coles.com.au using Selenium

    If you run this file it will scrape a sample of products - one page per subcategory.

    The Woolworths web scraper by default will scrape one page per category and will be faster to complete execution.

    We use several Javascript files. The Javascript is injected into a web page, extracts data and returns it as a JSON
    encoded string. Data is saved to the 'src/Datasets' folder as a JSON file with the name of the category.

    You can use get_all_categories() to get the names of categories which you can then scrape with scrape_products()

'''

import json, requests, time, random

# Import web scraping library
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

base_url = 'https://shop.coles.com.au/a/a-national/everything/browse/'

browser = webdriver.Chrome()

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
    ''' Returns a list of all top level / main product categories for Coles.com.au
    :return: list of all categories '''
    browser.get(base_url)
    return execute_script('scrape_categories.js')

def scrape_all_products(max_num_pages=float('inf')):
    ''' Scrape all products for all categories
    :param max_num_pages: the maximum number of pages to scrape for each category '''
    all_categories = get_all_categories()
    scrape_products(all_categories, max_num_pages)

def scrape_products(categories, max_num_pages=float('inf')):
    ''' Scrape data for all products under the categories provided and save as JSON file
    :param categories: the categories to scrape products for
    :param max_num_pages: the maximum number of pages to scrape for each category
    :return: none '''
    # Loop through categories
    for category in categories:

        # Tobacco category requires the user verify their age
        # If you wanted to scrape this category some Javascript could be used to get past this
        if category == 'tobacco':
            break

        # Construct URL for first page of this category
        url = base_url + category + '?pageNumber=1'

        # Coles does not list all products under the 'main' categories.
        # You have to click on a subcategory to view all products.
        # We use Javascript to retrieve the URL's for all of the subcategories
        browser.get(url)
        subcategories = execute_script('scrape_subcategory_urls.js')

        category_data = [] # accumulated data for all products in this category

        # Loop through all subcategories
        for sub in subcategories:

            # Format subcategory
            subcategory = sub.replace(base_url, '')
            subcategory = subcategory.replace('?pageNumber=1', '')
            subcategory = subcategory.replace('#', '')
            subcategory = subcategory.replace(category + '/', '')

            # Construct subcategory URL
            url = base_url + category + '/' + subcategory + '?pageNumber=1'

            # Get number of pages for this subcategory
            browser.get(url)
            num_pages = execute_script('get_num_pages.js')
            num_pages = int(num_pages)

            # Loop through all pages in subcategory
            for page_number in range(1, num_pages + 1):

                # Break if we have scraped the maximum desired number of pages for this subcategory
                if page_number > max_num_pages:
                    break

                # Get next page
                url = base_url + category + '/' + subcategory + '?pageNumber=' + str(page_number)
                browser.get(url)

                # Wait for products to be loaded
                # i.e. until the presence of HTML element with class 'product-list' is detected
                try:
                    timeout = 10
                    WebDriverWait(browser, timeout).until(EC.presence_of_element_located((By.CLASS_NAME, 'product-list')))
                except TimeoutException: # last page of category
                    pass

                # Extract all product data from this page
                page_data = execute_script('scrape_products.js')

                # Add category and subcategory to product JSON
                for product in page_data:
                    product['category'] = category
                    product['subcategory'] = subcategory

                # Add all products on this page to accumulative product data for this category
                category_data += page_data

                # Sleep so we don't overwhelm their website with requests
                time.sleep(random.randint(1,5))

        # Save product data for this category as JSON file
        filename = '../Datasets/Coles/' + category + '.json'
        save_json(filename, category_data)

if __name__ == '__main__':
    scrape_all_products()
