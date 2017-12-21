/*

    This script is injected when the crawler is started into the main URL:
    https://www.woolworths.com.au

    It gets the URL's for each category and then extracts the name of the category from the URL

    It returns a JSON encoded string - an array of category names

*/

var categories = [];

// All categories are contained in anchor elements with the class 'categoryHeader-navigationLink'
var category_elements = document.getElementsByClassName('categoryHeader-navigationLink');

// Loop through category anchor tags
for (var i=0; i < category_elements.length; i++) {
  // Get category URL
  var url = category_elements[i].href;
  // Extract category name from URL
  var category = url.replace('https://www.woolworths.com.au/shop/browse/', '')
  category = category.replace('http://www.woolworths.com.au/shop/browse/', '')
  categories.push(category);
}

return JSON.stringify(categories);
