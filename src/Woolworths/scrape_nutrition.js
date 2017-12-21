/*

    We don't currently use nutritional information in our data analysis.

    If you're marking this project I would not worry about looking at this code.

    This script retrieves the nutritional information for a single product on Woolworths.com.au

    Sometimes the nutritional information is incorrect or incorrectly formatted on the website - can't do much about this

    Also the majority of products do not have nutritional information

    It also requires exponentially more web requests to retrieve nutritional information than simply product data

*/

// Create JSON object to store nutrition data
var json = {};
json.nutrition = {};

// Get product description
var description = document.getElementsByClassName('viewMore');
if (description.length > 0) {
    json.description = description[0].textContent.trim()
}

// Get product 'ingredients'
var ingredients = document.querySelectorAll('[ng-bind-html="::$ctrl.detail.AdditionalAttributes.ingredients"]');
if (ingredients.length > 0) {
  json.ingredients = ingredients[0].textContent.trim();
}

// Get nutritional information
var nutrition = document.getElementsByClassName('productDetail-nutritionTable');
if (nutrition.length > 0) {

  // Get number of servings per package
  var servings = document.querySelectorAll('[ng-if="$ctrl.detail.NutritionalInformation[0].ServingsPerPack"]');
  if (servings.length > 0) {
    json.nutrition.servingsPerPack = servings[0].textContent.trim().replace("Servings per package: ", "");
  }

  // Get serving size
  var servingSize = document.querySelectorAll('[ng-if="$ctrl.detail.NutritionalInformation[0].ServingSize"]');
  if (servingSize.length > 0) {
    json.nutrition.servingSize = servingSize[0].textContent.trim().replace("Serving size: ", "");
  }

  // Get nutritional information - calories, carbohydrates, etc
  var nutritionTable = document.querySelectorAll('[ng-repeat="nutritionValue in ::$ctrl.detail.NutritionalInformation"]');
  for (var i=0; i < nutritionTable.length; i++) {
    if (nutritionTable[i].children.length == 3) {
        var nutrient = nutritionTable[i].children[0].textContent.trim(); // eg energy, sugar, protein etc
        json.nutrition[nutrient + ' per serving'] = nutritionTable[i].children[1].textContent.trim();
        json.nutrition[nutrient + ' per 100g'] = nutritionTable[i].children[2].textContent.trim();
    }
  }
}

return JSON.stringify(json);
