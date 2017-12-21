/*

    This script is injected on the first page of a subcategory - i.e. a URL of the form:
    https://shop.coles.com.au/a/a-national/everything/browse/category/subcategory?pageNumber=1

    It returns the total number of pages of products for this subcategory

*/


// All of the page numbers are contained in list items <li> with class 'page-number'
var page_numbers = document.getElementsByClassName('page-number');
if (page_numbers.length > 0) {
  // Get the last page
  var last_page = page_numbers[page_numbers.length-1];
  // Each page number list item has a 'number' class which contains the actual page number
  var last_page_num = last_page.getElementsByClassName('number')[0];
  return last_page_num.textContent;
}
else {
  // There are no items with class 'page-number'
  // i.e. there is only one page
  return '1';
}
