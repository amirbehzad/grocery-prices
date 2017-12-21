'''

    This is the main file that does all of the data processing, analysis and visualisation.

    If you run this file with Python it will read in the data for all products contained in JSON files in 'Datasets/Coles'
    and 'Datasets/Woolworths', then it will find products with similar names using scikit-learn and finally analyse the
    prices of these products and perform a t-distribution test to determine if there is a statistically significant
    difference in price between Woolworths and Coles as well as generating some visualisations.

'''

import json, re, os, scipy.stats, statistics
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation
from textwrap import wrap


class UnitPrice:
    '''
    This class represents the unit price of a product.

    A unit price has three components:
    - unit is a string either 'kg', 'grams' or 'each'.
    - quantity is an integer.
    - price is a float in dollars.

    So for example if the price of apples is $5 per kg then:
    price = 5, unit = 'kg', quantity = 1
    '''
    def __init__(self, price, unit, quantity):
        self.price = price
        self.unit = unit
        self.quantity = quantity

class Product:
    ''' This class represents a product including the product name, store (either Woolworths or Coles) and unit price '''
    def __init__(self, name, store, unit_price):
        self.name = name
        assert(store == 'Woolworths' or store == 'Coles')
        self.store = store
        assert(type(unit_price) == UnitPrice)
        self.unit_price = unit_price

class MatchedProduct:
    ''' This class represents a matched product - i.e. a pair of similar products from Coles and Woolworths
    Both products are of class Product and similarity is a float between 0 and 1 - how similar the product names are,
    higher means more similar. '''
    def __init__(self, woolworths_product, coles_product, similarity):
        self.woolworths_product = woolworths_product
        assert(type(woolworths_product) == Product)
        self.coles_product = coles_product
        assert(type(coles_product) == Product)
        self.similarity = similarity

def load_json(filename):
    ''' Open a file containing JSON and return the JSON as a dictionary or list
    :param filename: the name of the JSON file
    :return: JSON data - can be either a dictionary or list depending on the JSON structure '''
    f = open(filename, 'r')
    data = json.load(f)
    f.close()
    return data

def combine(directory):
    ''' Combine all JSON files in a directory into 'combined.json'
    Intended usage: combine('Datasets/Woolworths/') or combine('Datasets/Coles/')
    :param directory: the name of the directory
    :return: None '''
    files = os.listdir(directory) # list of all files in directory
    combined = [] # combined JSON data

    # Loop through all files
    for file in files:
        # If the file is a JSON file open it and add data to combined JSON
        if '.json' in file:
            f = open(directory + file, 'r')
            data = json.load(f)
            f.close()
            combined += data

    # Save combined JSON file
    f = open(directory + 'combined.json', 'w+')
    json_string = json.dumps(combined, indent=4, sort_keys=True)
    f.write(json_string)
    f.close()

def combine_woolworths():
    ''' Combine all JSON files in Datasets/Woolworths into combined.json'''
    combine('Datasets/Woolworths/')

def combine_coles():
    ''' Combine all JSON files in Datasets/Coles into combined.json '''
    combine('Datasets/Coles/')

def histogram(data, title, xlabel, ylabel, text=None, text_x=0.5, text_y=0.5):
    ''' Create and display a histogram with matplotlib
    It uses one bin for every 4 data points which is fine for the datasets we are working with.
    :param data: data to use for histogram
    :param text: description text to display on the histogram
    :param title : title to display
    :param xlabel: x axis label to display
    :param ylabel: y axis label to display
    :param text_x: horizontal displacement of text
    :param text_y: vertical displacement of text '''

    fig = plt.figure()
    ax = fig.add_subplot(111)

    # Add description text if provided
    if text:
        plt.text(text_x, text_y, text, horizontalalignment='left', verticalalignment='center', transform = ax.transAxes)

    # Create histogram with title and axis labels
    num_bins = int(len(data)/4)
    ax.hist(data, num_bins)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.show()

def paired_data_test(differences):
    ''' Note: we are not statisticians, our comment here might not be helpful, feel free to ignore it
    With the sample data we used we believe there was not a statistically significant difference in prices

    This function performs a paired data t-distribution test using the price differences for matched products

    The following is an excerpt from OpenIntro Statistics Chapter 5.2, page 228 on 'paired data':

    "Two sets of observations are paired if each observation in one set has a special correspondence or connection with
    exactly one observation in the other data set... To analyze paired data, it is often useful to look at the difference
    in outcomes of each pair of observations... Using differences between paired observations is a common and useful way
    to analyze paired data... To analyze a paired data set, we simply analyze the differences. We can use the same
    t-distribution techniques we applied in the last section."

    The Woolworths and Coles price of each matched product is a pair of observations. In order to analyse and test
    hypotheses about the prices we analyse the difference of each pair. For each matched product we look at the Woolworths
    price minus the Coles price - the 'differences' parameter is a list of these price differences.

    In order to use a t-distribution the data has to be a simple random sample of less than 10 percent of the population
    and the data has to be roughly normal although as the sample size increases this becomes less important.

    We pass 0.0 as the popmean parameter to the scipy t-test function.

    What this means is Scipy will perform a hypothesis test to determine the probability the population mean is equal to zero.
    If the population mean was equal to zero the difference in prices, Woolworths minus Coles would be equal to zero.
    So we're testing the probability there is a difference in prices.

    Our null hypothesis is that there is no difference in price between Woolworths and Coles:
    H0: μ diff = 0
    Woolworths price - Coles price = 0

    Our alternative hypothesis is that there is a difference in price between Woolworths
    HA: μ diff != 0
    Woolworths price - Coles price != 0
    There is a difference in price

    The documentation for Scipy's one sample t-test function:
    https://docs.scipy.org/doc/scipy-0.15.1/reference/generated/scipy.stats.ttest_1samp.html

    :param differences: the price difference for each matched product, Woolworths price minus Coles price '''

    # Print some information to the console about the price differences
    total_difference = sum(differences)
    num_similar_products = len(differences)
    print('Number of similar products found: ' + str(num_similar_products))
    print('Total difference in price, woolworths - coles: ' + str(total_difference))
    if total_difference < 0:
        print('Woolworths wins')
    elif total_difference == 0:
        print('Draw')
    else:
        print('Coles wins')

    # Perform statistical test
    diff_array = np.array(differences)
    popmean = 0.0
    t_statistic, two_sided_pvalue = scipy.stats.ttest_1samp(diff_array, popmean, axis=0)
    print('t-score: ' + str(t_statistic))
    print('two sided p-value: ' + str(two_sided_pvalue))

    if two_sided_pvalue < 0.05:
        print('two sided p-value < 0.05')
        print('i.e. we reject the null hypothesis that the population difference is equal to 0')
        print('we reject the claim that there is no difference')
    else:
        print('p-value > 0.05')
        print('we fail to reject the null hypothesis')
        print('there is not enough evidence to support a difference in price')

    # Create histogram of price differences with p-value and test statistic
    txt  = 'n = ' + str(len(differences)) + '\n'
    txt += 'sample mean = ' + str(round(statistics.mean(differences),2)) + '\n'
    txt += 'sample stdev = ' + str(round(statistics.stdev(differences),2)) + '\n'
    txt += 't-score: ' + str(round(t_statistic,2)) + '\n'
    txt += 'two sided p-value: ' + str(round(two_sided_pvalue,2)) + '\n'
    title='Price Difference of Matched Products'
    xlabel='Woolworths price - Coles price'
    ylabel='# occurrences'
    histogram(differences, title, xlabel, ylabel, txt, text_x=0.1, text_y=0.7)

def convert_unit_price(s):
    ''' This function takes a string representing the unit price of a product and parses the string into data that we can
    work with. It returns a three tuple (price, unit, quantity) where price and quantity are numbers and unit is a string
    with a value of of 'kg', 'grams', or 'each'. This function only works with the format of strings used on Woolworths.com.au
    and Coles.com.au. If it fails to parse the string and an exception is thrown it returns None.

    For example if apples cost $5 per kg this would be represented as:
    price = 5, unit = 'kg', quantity = 1

    If Rosemary is $2 per 10 grams this would be represented as:
    price = 2, unit = 'grams', quantity = 10

    Coles and Woolworths use the following formats for the parameter 's':
    "$price per unit"
    "$price / unit"

    where unit is one of 'kg', 'g', 'ea' or 'each' and price is a float

    :param s: unit price string formatted according to rules outlined above
    :return: tuple (price, unit, quantity) where unit is a string - either 'kg', 'grams', 'each', quantity and price are floats '''

    try:

        # Split string with either 'per' or '/'
        if ' per ' in s:
            l = s.split(' per ')
        elif ' / ' in s:
            l = s.split(' / ')
        else:
            return None

        price_string = l[0] # a string "$price"
        price = float(price_string[1:]) # splice away dollar sign

        unit_and_quantity = l[1] # a string - '10kg', '50g', 5 each', etc
        unit_and_quantity = unit_and_quantity.lower()

        # Branch on unit and extract quantity from string
        if 'kg' in unit_and_quantity:
            quantity = float(unit_and_quantity.replace('kg', ''))
            unit = 'kg'
            return (price, quantity, unit)
        elif 'ea' in unit_and_quantity or 'each' in unit_and_quantity:
            quantity = float(unit_and_quantity.replace('ea', '').replace('each', ''))
            unit = 'each'
            return (price, quantity, unit)
        elif 'g' in unit_and_quantity:
            quantity = float(unit_and_quantity.replace('g', ''))
            unit = 'grams'
            return (price, quantity, unit)
        else:
            # This try block seemed to help parse a few products that were causing exceptions
            try:
                quantity = float(unit_and_quantity)
                unit = 'ea'
            except ValueError:
                quantity = 'unknown'
                unit = 'unknown'
            return (price, quantity, unit)
    except Exception:
        return None

def text_similarity(string, list_of_strings):
    ''' This function is used to find the text similarity between a string and every element in a list of strings

    This function is passed the name of a product from one store (string) and a list of names of all products from another
    store (list_of_strings). It computes the text similarity between the individual product and all products in the list.

    It returns a list of floats - where the (i+1)th element is the similarity between 'string' and the ith element of
    'list_of_strings', the similarity is between 0 and 1, where higher is more similar.

    :param string: a string - the name of a product from one store
    :param list_of_strings: a list of strings - names of products from the other store
    :return: a list where the (i+1)th element is the similarity between 'string' and ith element of 'list_of_strings'
    the first element of the list is 1.0 - the similarity between 'string' and itself '''

    strings = [string] + list_of_strings

    # This code is based on the following discussion on StackOverflow:
    # https://stackoverflow.com/questions/8897593/similarity-between-two-text-documents/8897648#8897648
    vect = TfidfVectorizer(min_df=1)
    tfidf = vect.fit_transform(strings)

    # similarity_array is a Numpy ndarray where position (i, j) is the similarity between element i and j of strings
    similarity_array = (tfidf * tfidf.T).A

    # Get the first column as a list - we only care about the first column because this gives us the similarity between
    # 'string' and every element in list_of_strings. We don't care about similarity between products from the same store.
    first_column = similarity_array[:,:1]
    return first_column.tolist()

def barplot_animated(woolworths_prices, coles_prices, matched_product_names):
    ''' Create animated bar plot displaying price at Coles and Woolworths for each matched product

    This code is based on the following discussions on StackOverflow.
    https://stackoverflow.com/a/42143866
    https://stackoverflow.com/a/34372367

    woolworths_prices, coles_prices and matched_product_names are lists where the ith element of each list correspond to
    each other. For the ith product woolworths_prices[i] is it's price at Woolworths, coles_prices[i] is it's price at
    Coles and matched_product_names[i] is a tuple where the first element is the name of the product at Coles and the
    second element is the name at Woolworths. '''

    # Setup plot, title, and y-label
    fig, ax = plt.subplots()
    ax.set_title('Matched Products')
    ax.set_ylabel('Price ($)')

    width = 0.5 # set width of the bars
    x_location = [1,2] # set x-axis location of bars

    # Create bar plot 'initialized' with the first matched product
    # Set height of bars to the prices of the first matched product
    first_item_prices = [coles_prices[0], woolworths_prices[0]]
    barlist = ax.bar(x_location, first_item_prices, width)

    # Set x-tick labels to the names of the first matched product
    ax.set_xticks(x_location)
    coles_name = matched_product_names[0][0]
    woolworths_name = matched_product_names[0][1]
    ax.set_xticklabels((coles_name + '\n(Coles)', woolworths_name + '\n(Woolworths)'))

    # Set color of Coles bar to red and Woolworths bar to green
    barlist[0].set_color('r')
    barlist[1].set_color('g')

    # Set the height of the barplot to the maximum price of any product
    plt.ylim(0, max(coles_prices + woolworths_prices))

    def animate(i):
        ''' Called once for each pair of matched products, sets height of bars and updates x-tick labels
        :param i: integer between 0 and number of matched products - 1, corresponding to the ith matched product '''

        # Set the height of the bars to the prices of the ith matched products
        barlist[0].set_height(coles_prices[i])
        barlist[1].set_height(woolworths_prices[i])

        # Set the x-tick labels to the names of the ith matched products
        coles_product_name = matched_product_names[i][0]
        woolies_product_name = matched_product_names[i][1]

        # Wrap long product names over multiple lines
        coles_label = '\n'.join(wrap(coles_product_name, 25)) + '\n(Coles)'
        woolworths_label = '\n'.join(wrap(woolies_product_name, 25)) + '\n(Woolworths)'

        ax.set_xticklabels((coles_label, woolworths_label))

        return barlist

    # Start bar plot animation
    anim = animation.FuncAnimation(fig, animate, frames=len(matched_product_names), interval=2000)
    plt.show()

def scatter_plot_3D(x, y, z, title, xlabel, ylabel, zlabel):
    ''' Create a basic 3D scatter plot with title and axis labels
    Based on an example from the official matplotlib documentation:
    https://matplotlib.org/examples/mplot3d/scatter3d_demo.html
    :param x: the x axis data points
    :param y: the y axis data points
    :param z: the z axis daata points
    :param title: the title of the plot
    :param xlabel: the x axis label
    :param ylabel: the y axis label
    :param zlabel: the z axis label '''

    # Boilerplate
    from mpl_toolkits.mplot3d import Axes3D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Create scatter plot and set title and axis labels
    ax.scatter(x, y, z)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_zlabel(zlabel)
    plt.show()

def analysis_and_visualisation(matching_products, all_woolworths_prices, all_coles_prices):

    # lists of prices of matched products
    woolworths_matched_prices = [matched_product.woolworths_product.unit_price.price for matched_product in matching_products]
    coles_matched_prices = [matched_product.coles_product.unit_price.price for matched_product in matching_products]

    # list of price difference of matched products, Woolworths price minus Coles price
    differences = [matched_product.woolworths_product.unit_price.price - matched_product.coles_product.unit_price.price for matched_product in matching_products]

    # list of similarity scores for matched products
    similarities = [matched_product.similarity for matched_product in matching_products]

    # list of matched product names
    matched_product_names = [(matched_product.coles_product.name, matched_product.woolworths_product.name) for matched_product in matching_products]

    # Create histogram of all Woolworths prices (not just matched products) displaying mean, median, stddev, etc
    txt =  'n = ' + str(len(all_woolworths_prices)) + '\n'
    txt += 'mean   = $' + str(round(statistics.mean(all_woolworths_prices),2)) + '\n'
    txt += 'median = $' + str(round(statistics.median(all_woolworths_prices),2)) + '\n'
    txt += 'standard deviation = $' + str(round(statistics.pstdev(all_woolworths_prices),2)) + '\n'
    title='All Woolworths Product Prices'
    xlabel='Price ($)'
    ylabel='# products'
    histogram(all_woolworths_prices, title, xlabel, ylabel, txt, text_x=0.5, text_y=0.5)

    # Create histogram of all Coles prices (not just matched products) displaying mean, median, stddev, etc
    txt =  'n = ' + str(len(all_coles_prices)) + '\n'
    txt += 'mean   = $' + str(round(statistics.mean(all_coles_prices),2)) + '\n'
    txt += 'median = $' + str(round(statistics.median(all_coles_prices),2)) + '\n'
    txt += 'standard deviation = $' + str(round(statistics.pstdev(all_coles_prices),2)) + '\n'
    title='All Coles Product Prices'
    xlabel='Price ($)'
    ylabel='# products'
    histogram(all_coles_prices, title, xlabel, ylabel, txt, text_x=0.5, text_y=0.5)

    # Create scatter plot for prices of matched products, Woolworths price on x-axis, Coles price on y-axis
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(woolworths_matched_prices, coles_matched_prices)
    ax.set_title('Matched Products')
    ax.set_xlabel('Woolworths price ($)')
    ax.set_ylabel('Coles price ($)')
    txt = 'n = ' + str(len(woolworths_matched_prices))
    plt.text(0.1, 0.9, txt, horizontalalignment='left', verticalalignment='center', transform = ax.transAxes)
    plt.show()

    # Create scatter plot for price difference and similarity score
    # A lower similarity score is associated with higher variance in price
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(differences, similarities)
    ax.set_title('Price Difference vs Similarity')
    ax.set_xlabel('Price Difference, Woolworths - Coles ($)')
    ax.set_ylabel('Similarity [0.0,1.0]')
    plt.show()

    # Create 3D scatter plot displaying matched product prices and similarity score
    # SHows the same association above but on a 3D plot
    scatter_plot_3D(x=woolworths_matched_prices, y=coles_matched_prices, z=similarities, title='Matched Products', \
        xlabel='Woolworths price ($)', ylabel='Coles price ($)', zlabel='Similarity Score [0.0,1.0]')

    # Perform statistical hypothesis test
    paired_data_test(differences)

    # Create animated bar plot displaying names and prices of each matched product
    barplot_animated(woolworths_matched_prices, coles_matched_prices, matched_product_names)

def read_product_json(filename):
    ''' Read in product data from JSON file and turn it into a dictionary using product name as key (to make sure there
    aren't any duplicates) and the product data as value. The product data is a dictionary.
    :param filename: the JSON file to read in
    :return: dictionary - key is product name, value is product JSON (another dictionary) '''

    # Load JSON data from file
    file_data = load_json(filename)
    products = {}

    # Loop through all products
    for product in file_data:
        # some products don't have names for some reason
        # we're only interested in products with names
        if 'name' in product:
            # Add product to dictionary
            products[product['name']] = product

    return products

def find_matching_products(woolworths, coles, similarity_threshold = 0.5, print_to_console=True):
    ''' This function takes two dictionaries of Woolworths and Coles products, as returned by read_product_json(), and
    finds products with similar names using the similarity threshold.

    :param similarity_threshold: float between 0 and 1, how 'similar' product names must be in order to match,
                                 0 is completely different and 1 is identical, passed directly to scikit-learn TFIDF

    :param woolworths: a dictionary of Woolworths products as returned by read_product_json()
                       the key is the product name, the value is the product data

    :param coles: a dictionary of Coles products as returned by read_product_json()
                  the key is the product name, the value is the product data

    :param print_to_console: boolean, whether or not to print information to console as data is processed

    :return: list of MatchedProduct objects '''

    coles_names = list(coles.keys()) # list of names of all Coles products

    matching_products = [] # list of MatchedProduct objects

    # Iterate through all Woolworths products
    for woolworths_product_name, woolworths_product_value in woolworths.items():

        # Compute text similarity for the current Woolworths product and all Coles products
        similarity_scores = text_similarity(woolworths_product_name, coles_names)

        # Iterate through all Coles products
        for i in range(len(coles_names)):

            # Lookup similarity for current Woolworths product and ith Coles product
            similarity = similarity_scores[i+1][0]

            # If similarity > threshold, the products are similar enough to compare prices
            if similarity > similarity_threshold:

                # When Coles products are on special they don't include the normal price
                # So if a Coles product is on special we don't won't to include it in the comparison
                coles_not_on_special = coles[coles_names[i]]['special'] != 'True'
                if coles_not_on_special:

                    # Get unit price for matched Coles product
                    coles_unit_price = convert_unit_price(coles[coles_names[i]]['price'])
                    if coles_unit_price is None: break
                    coles_price = coles_unit_price[0]
                    coles_quantity = coles_unit_price[1]
                    coles_unit = coles_unit_price[2]
                    coles_unit_price = None

                    # Print to console
                    if print_to_console:
                        print('Similarity: ' + str(similarity))
                        print('Coles product: ' + coles_names[i])
                        print('Woolworths product: ' + woolworths_product_name)
                        print('Coles price: $' + str(coles_price) + ' per ' + str(coles_quantity) + ' ' + coles_unit)

                    # We can only compare products if we have their unit price
                    if 'unitPrice' in woolworths_product_value:

                        # Get unit price for matched Woolworths product
                        woolworths_price, woolworths_quantity, woolworths_unit = convert_unit_price(woolworths_product_value['unitPrice'])

                        if print_to_console:
                            print('Woolworths price: $' + str(woolworths_price) + ' per ' + str(woolworths_quantity) + ' ' + woolworths_unit)


                        woolworths_unit_price = None
                        coles_unit_price = None

                        # if products are of the same unit e.g. 'kg', 'g', 'ea'
                        if woolworths_unit == coles_unit:

                            # if the products also have the same quantity e.g. 1 kilogram, 10 grams, etc
                            # then we can directly compare prices
                            if woolworths_quantity == coles_quantity:

                                woolworths_unit_price = UnitPrice(woolworths_price, woolworths_unit, woolworths_quantity)
                                coles_unit_price = UnitPrice(coles_price, coles_unit, coles_quantity)

                                if print_to_console:
                                    print('Difference: ' + str(woolworths_price - coles_price))

                            else: # products have same unit but different quantities

                                # This code uses some simple math to convert the price and quantites so the products
                                # can be compared. This only works if one quantity is perfectly divisible by the other.
                                # i.e. the quantities are multiples.

                                woolworths_div_coles = woolworths_quantity // coles_quantity
                                coles_div_woolworths = coles_quantity // woolworths_quantity
                                if woolworths_div_coles > 0: # Woolworths quantity is larger than Coles quantity
                                    if woolworths_quantity % coles_quantity == 0:
                                        # the woolworths quantity is perfectly divisible by the coles quantity
                                        coles_quantity *= woolworths_div_coles
                                        coles_price    *= woolworths_div_coles

                                        woolworths_unit_price = UnitPrice(woolworths_price, woolworths_unit, woolworths_quantity)
                                        coles_unit_price = UnitPrice(coles_price, coles_unit, coles_quantity)

                                        if print_to_console:
                                            print('Difference: ' + str(woolworths_price - coles_price))

                                # This elif block is exactly the same as the above if block, but vice versa for Coles/Woolworths
                                elif coles_div_woolworths > 0:
                                    if coles_quantity % woolworths_quantity == 0:
                                        woolworths_quantity *= coles_div_woolworths
                                        woolworths_price    *= coles_div_woolworths
                                        woolworths_unit_price = UnitPrice(woolworths_price, woolworths_unit, woolworths_quantity)
                                        coles_unit_price = UnitPrice(coles_price, coles_unit, coles_quantity)
                                        if print_to_console:
                                            print('Difference: ' + str(woolworths_price - coles_price))

                    # If the Woolworths and Coles unit prices are set we were able to convert to the same unit and quantity
                    # meaning we can compare the prices, so we add the products to the list of matched products
                    if woolworths_unit_price and coles_unit_price:
                        # Create Product objects for Woolies and Coles product
                        woolworths_product = Product(woolworths_product_name, 'Woolworths', woolworths_unit_price)
                        coles_product = Product(coles_names[i], 'Coles', coles_unit_price)
                        # Create MatchedProduct object and add it to list of matched products
                        matched_product = MatchedProduct(woolworths_product, coles_product, similarity)
                        matching_products.append(matched_product)

                    # Print separator between each product
                    if print_to_console:
                        print('\n===========================================\n')

    return matching_products

def compare_products(woolworths_filename, coles_filename, similarity_threshold=0.5):
    ''' Read in data for all Woolworths and Coles products contained in JSON files provided as parameters
    Call functions to find matching Coles and Woolworths products, analyse data and visualise results
    :param woolworths_filename: the name of the JSON file containing Woolworths products
    :param coles_filename: the name of the JSON file containing Coles products
    :param similarity_threshold: the similarity threshold to use when finding products with similar names '''

    # Read product data from JSON files into dictionaries
    woolworths = read_product_json(woolworths_filename)
    coles = read_product_json(coles_filename)

    # Get the prices of all Woolworths products and all Coles products, not just matching products, only used for visualisation
    all_woolworths_prices = [product['price'] for product in woolworths.values()]
    all_coles_prices = [convert_unit_price(product['price'])[0] for product in coles.values() if convert_unit_price(product['price'])]

    # Find matching products using similarity threshold
    matching_products = find_matching_products(woolworths, coles, similarity_threshold)

    # Create visualisaations and perform statistical tests
    analysis_and_visualisation(matching_products, all_woolworths_prices, all_coles_prices)

def compare_all_products(similarity_threshold=0.5):
    ''' Compare prices of Woolworths and Coles using all JSON files in 'Datasets/Woolworths' and 'Datasets/Coles'
    :param similarity_threshold: float between 0 and 1 given to scikit-learn TfidfVectorizer, a higher threshold means
    a Coles and Woolworths product names must be more similar in order to be considered similar products and to compare prices '''

    # Combine all JSON files
    combine_woolworths()
    combine_coles()
    woolworths_filename = 'Datasets/Woolworths/combined.json'
    coles_filename = 'Datasets/Coles/combined.json'

    # Run code to find similar products, analyse data and produce visualisations
    compare_products(woolworths_filename, coles_filename, similarity_threshold)

if __name__ == '__main__':
    compare_all_products()
