/*

  This script is injected into a page of the form:
  https://www.woolworths.com.au/shop/browse/fruit-veg?pageNumber=1

  It finds all products on the page and gets relevant information including:
  - price
  - name
  - unit price (price per kg, 100g)
  - if the product is on special
  - product URL on Woolworths.com.au
  - product image URL, image filename
  - URL of next page in this category of products

  The price is always the non-discounted price. Even if the product is on special this is sometimes displayed.

  It returns the data as a JSON encoded string.

  Below is a description of all the fields of the JSON object:

  {
    numProducts - the number of products on this page (number)
    products    - array of all products on this page (array)
    nextPage    - the URL of the next page of products in this category (text)
  }

  Each element of the products array is a JSON object with the following structure:

  {
    name      - the name of the product               (text)
    price     - the price of the product in dollars   (number)
    href      - the product URL on Woolworths.com.au  (text)
    imgSrc    - the source URL of the product image   (text)
    imgName   - the filename of the product image     (text)
    unitPrice - the unit price (per kg, 100g) of the product      (text)
    special   - the discounted price if the product is on special (number)
  }

  Not all of the fields are provided for every product.

  For example if the product is on special sometimes the ordinary price is not displayed so this may be null.

  Also many products don't display unit prices or do not have images.

*/

// Create JSON object to store product data and page metadata (i.e. number of products)
var json = {};
json.products = [];
json.numProducts = json.products.length; // not currently using this

// All products are contained in divs with the class 'shelfProductTile-content'
var products = document.getElementsByClassName('shelfProductTile-content');

// Loop through all products on the page
for (var i=0; i < products.length; i++) {

  var product = products[i]; // the product's HTML element
  var productJson = {};      // the JSON we are constructing for this product

  // Get product name and URL
  var descriptionLink = product.getElementsByClassName('shelfProductTile-descriptionLink');
  if (descriptionLink.length > 0) {
    productJson['href'] = descriptionLink[0].href;
    productJson['name'] = descriptionLink[0].textContent.trim();
  }

  // Get product price
  var priceDollars = product.getElementsByClassName('price-dollars');
  var priceCents = product.getElementsByClassName('price-cents');
  if (priceDollars.length > 0 && priceCents.length > 0) {
    productJson['price'] = Number(priceDollars[0].textContent + '.' + priceCents[0].textContent);
  }
  // Check if product is on special and original price is displayed
  var normalPrice = product.getElementsByClassName('shelfProductTile-wasPrice');
  if (normalPrice.length > 0) {
    normalPrice = normalPrice[0].textContent.trim();
    normalPrice = Number(normalPrice.replace('Was $', ''));
    productJson['special'] = productJson['price'];
    productJson['price'] = normalPrice;
  }
  else {
    // Check if product is on special and original price is not displayed
    var special = product.querySelectorAll('[alt="On Special"]');
    if (special.length > 0) {
      productJson['special'] = productJson['price'];
      delete productJson['price'];
    }
  }

  // Get product unit price
  var unitPrice = product.getElementsByClassName('shelfProductTile-cupPrice');
  if (unitPrice.length > 0) {
    productJson['unitPrice'] = unitPrice[0].textContent.trim();
  }

  // Get product image URL - not currently using this
  // Is image name even useful?
  var img = product.getElementsByClassName('shelfProductTile-image');
  if (img.length > 0) {
    productJson['imgSrc'] = img[0].src;
    var re = /(\d|[a-z]|[A-Z])+(\.jpg|\.png)/g; // regex to match jpg and png image names from image source URL
    var matches = productJson['imgSrc'].match(re);
    if (matches != null && matches.length > 0) {
      productJson['imgName'] = matches[0];
    }
  }

  json.products.push(productJson);
}

// Get URL of next page in category
var nextPage = document.getElementsByClassName('paging-next _pagingNext');
if (nextPage.length > 0) json.nextPage = nextPage[0].href;
else json.nextPage = 'NONE';

return JSON.stringify(json);
