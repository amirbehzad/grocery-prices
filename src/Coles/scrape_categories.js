/*

    This script is injected when the crawler is started into the main URL:
    https://shop.coles.com.au/a/a-national/everything/browse/

    It retrieves the names (not URL's) of all of the 'top level' or 'main' categories

*/

var categories = [];

// All of the categories are within 'cat-nav-item' divs
var category_elements = document.getElementsByClassName('cat-nav-item')

// Loop through all of the category divs
for (var i=0; i < category_elements.length; i++) {
  // Each div has a single child - an anchor tag with an href attribute
  var anchor_tag = category_elements[i].children[0];
  var url = anchor_tag.href;
  // We just want the category name so we use replace() to remove unwanted text from the URL
  var category = url.replace('https://shop.coles.com.au/a/a-national/everything/browse/', '');
  category = category.replace('?pageNumber=1', '');
  categories.push(category);
}

return JSON.stringify(categories);
