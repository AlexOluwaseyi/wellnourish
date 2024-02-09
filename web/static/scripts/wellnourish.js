$(document).ready(() => {
    $.get('http://0.0.0.0:5001/api/v1/recipes', function (data) {
	let len = data.recipes.length
	/*console.log(data.recipes)*/
	for (let recipe of data.recipes) {

	       let ingrList = []
	       for (let ingr of recipe.extendedIngredients) {
		   ingrList.push(ingr.name)
	       }

	       $('.result-count h4').text(`Popular Recipes (${len})`)
	       recipeTile = `<li id=${recipe.id}>
	               <div class="list-img"></div>
	               <div class="list-title">
	                 <h3>${recipe.title}</h3>
	                 <p><b>Ingredients:</b> ${Object.values(ingrList).join(', ')}</p>
                         <p><b>Health Score:</b> ${recipe.healthScore}% </p>
                         <p><b>Rating:</b> ${recipe.spoonacularScore}%</p>
	               </div>
	              </li>`
 	       $('ul.recipes').append(recipeTile);
	    $(`#${recipe.id} .list-img`).css('background-image', `url(${recipe.image})`);

	}
    });
});
