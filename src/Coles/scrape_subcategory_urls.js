/*

  There are 'main' categories and 'subcategories' of products on Coles website

  For example a subcategory of dairy could be yoghurt.

  Coles does not list all of it's products under the main categories.

  You have to click on a subcategory to view all of the products.

  This script is injected into the page of a main category and returns a list of the URL's of all subcategories.

  This script is injected into URL's of the form: https://shop.coles.com.au/a/a-national/everything/browse/category

*/

var subcategories = [];

// Find divs with the class 'cat-nav-item' - these divs contain the subcategory URL's
var subcategory_elements = document.getElementsByClassName('cat-nav-item');

// Loop through the divs
for (var i=0; i < subcategory_elements.length; i++) {
  // Each div has exactly one child - an anchor tag whose 'href' attribute is the subcategory URL
  var anchor_tag = subcategory_elements[i].children[0];
  var url = anchor_tag.href;
  subcategories.push(url);
}

// Return the subcategory URL's as a JSON string
return JSON.stringify(subcategories);
