/*

    This script is injected onto a page containing products and retrieves information about each product including:
    - Product name (string)
    - Unit price (string)
    - Brand (string)
    - Package size (string)
    - Whether or not the product is on special (string - 'True' or 'False')
    - Product URL
    - Product image URL

    Here is an example of the JSON for a product:
    {
      "name":"Natural Almonds Prepacked",
      "brand":"Coles",
      "price":"$22.50 per 1Kg",
      "package_size":"400g",
      "url":"https://shop.coles.com.au/a/a-national/product/coles-natural-almonds-prepacked",
      "image_url":"https://shop.coles.com.au/wcsstore/Coles-CAS/images/2/1/2/2123599-th.jpg",
      "special":"False"
    }

    The Python script this JSON is returned to also appends a category and subcategory attribute to the JSON.

    This script is injected into pages of the form (where category and subcategory are replaced with actual values):
    https://shop.coles.com.au/a/a-national/everything/browse/category/subcategory?pageNumber=1

*/

var products = []; // array of all products on this page

// All of the products are contained in a 'product-list' HTML section
var product_list = document.getElementById('product-list');

// Loop through all products in product_list
for (var i=0; i < product_list.childElementCount; i++) {
  var product = {}; // the current product JSON we are constructing
	var product_element = product_list.children[i]; // the current product HTML element

  // Get product name
  var product_name  = product_element.getElementsByClassName('product-name');
  if (product_name.length > 0) {
      product['name']  = product_name[0].textContent.trim();
  }

  // Get product brand
  var brand = product_element.getElementsByClassName('product-brand');
  if (brand.length > 0) {
    product['brand'] = brand[0].textContent.trim();
  }

  // Get product price
  var price = product_element.getElementsByClassName('package-price');
  if (price.length > 0)
    product['price'] = price[0].textContent.trim();

  // Get package size
  var package_size = product_element.getElementsByClassName('package-size');
  if (package_size.length > 0)
    product['package_size'] = package_size[0].textContent.trim();

  // Get product URL
  var url = product_element.querySelectorAll('[data-ng-click="productTileVM.openProduct($event)"]');
  if (url.length > 0) {
    product['url'] = url[0].href;
  }

  // Get product image URL
  var img = product_element.getElementsByTagName('img');
  if (img.length > 0) {
    product['image_url'] = img[0].src;
  }

  // Check whether the product is on special by checking for the presence of the 'product-specials' div
  var special = product_element.getElementsByClassName('product-specials');
  if (special.length > 0)
    product['special'] = 'True';
  else
    product['special'] = 'False';

  // Add this product to list of products
  products.push(product);

}

return JSON.stringify(products);
