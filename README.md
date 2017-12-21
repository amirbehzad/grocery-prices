# Woolworths and Coles web scraper

This was a project I completed for university where I attempted to compare prices of Woolworths and Coles.

I am a programmer, not a statistician, so take my statistical analysis with a grain of salt.

I scraped the data from Woolworths and Coles websites using Selenium since the content is rendered dynamically and you
can't use 'requests' to scrape Javascript rendered content.

Selenium is also used for bots, automation, web site testing, etc.

The browser is controlled by Python and I inject Javascript which locates the content on the page to be scraped,
manipulating the HTML and returning a JSON encoded string.

I used scikit learn to find products with similar names and then compare prices using scipy.stats t-test

# Installation / Setup

In order to run our project, you will need to install the Selenium Python library and place a ChromeDriver executable on your path.

You will also need to have Chrome installed.

It may also work with Chromium but we have not tested this.

Selenium can be installed using pip using the command 'pip install selenium'.

If you do not have pip we recommend installing Anaconda which includes pip and a number of other libraries.

ChromeDriver can be downloaded from https://sites.google.com/a/chromium.org/chromedriver/downloads

Once you have the ChromeDriver executable this needs to be placed on your path.

We recommend simply placing it in your anaconda bin directory.

Alternatively on Unix systems it can be placed in '/usr/bin' and on Windows in 'C:/Windows/System32'

# Code Overview

The 'src' directory contains all code as well as some sample data sets.

We chose to include some sample data sets because while we do retrieve our data programatically it can take quite a while to run because we are scraping the data not using an API.

The main file that does the analysis and visualisation of results is 'src/process.py'

If you run this file with Python it will analyse all the JSON files in the 'src/Datasets' folder and generate some visualisations.

All of the code in 'src/Woolworths' and 'src/Coles' is web scraping code. The Javascript files are helper code that is injected into a web page to retrieve data and returns it to the Python program. 'src/Woolworths/scrape_woolworths.py' is the main file that scrapes data from Woolworths and 'src/Coles/scrape_coles.py' is the main file that scrapes data from Coles. If you run either of these files with Python it will start Selenium and begin scraping a sample of products, one page per category for Woolworths and one page per subcategory for Coles.

Please note you cannot modify the folder structure or the program will not work and all datasets should be JSON files located in either the 'src/Datasets/Woolworths' or 'src/Datasets/Coles' directories.

# Links

[Scraping a JS Rendered Page Using Python](http://stanford.edu/~mgorkove/cgi-bin/rpython_tutorials/Scraping_a_Webpage_Rendered_by_Javascript_Using_Python.php)

[Text similarity using scikit-learn](https://stackoverflow.com/a/8897648)

[Difference of means hypothesis test](http://stattrek.com/hypothesis-test/difference-in-means.aspx?Tutorial=AP)

- The code for the 3D scatter plot is based on the following example from the matplotlib documentation:
  https://matplotlib.org/examples/mplot3d/scatter3d_demo.html
  (URL also provided in source code)

- The code for using scikit-learn's TfidfVectorizer is based on the following solution we found when researching the problem:
  https://stackoverflow.com/a/8897648
  (URL also provided in source code)

- The code for the animated barplot is based on the following solutions we found when researching the problem:
  https://stackoverflow.com/a/42143866
  https://stackoverflow.com/a/34372367
  (URLs also provided in source code)

- The reasoning behind my statistical analysis / hypothesis testing and conclusions was based on the textbook OpenIntro
  Statistics, specifically Chapter 5.2 page 228. The textbook is open source and available on Google Drive.
  https://www.openintro.org/stat/textbook.php
  https://drive.google.com/file/d/0B-DHaDEbiOGkc1RycUtIcUtIelE/view?usp=sharing
