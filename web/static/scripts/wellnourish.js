$(document).ready(() => {
    $.get('http://0.0.0.0:5001/api/v1/recipes', function (data) {
	let len = data.length;
	console.log(data);
	for (let recipe of data) {
	    if (recipe.spoonacularScore >= 50) {
		let ingrList = [];
	       for (let ingr of recipe.extendedIngredients) {
		   ingrList.push(ingr.name);
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
	}
    });

    $('.search-button').on('click', function () {
	$('.result-tiles ul').empty();
	let ingrs = $('.search-box input').val();
	$.get(`http://0.0.0.0:5001/api/v1/recipes/find_by_ingr/${ingrs}`, function (recipe) {
	    let len = recipe.length;
	    console.log(recipe);
	    for (let i = 0; i < len; i++) {
		let ingrList = [];
		/*for (let ingr of recipe[i].usedIngredients) {
		    ingrList.push(ingr.name);
		}*/
		for (let ingr of recipe[i].missedIngredients) {
		    ingrList.push(ingr.name);
		}
		$('.result-count h4').text(`Results (${len})`)
		recipeTile = `<li id=${recipe[i].id}>
	               <div class="list-img"></div>
	               <div class="list-title">
	                 <h3>${recipe[i].title}</h3>
	                 <p><b>Missing Ingredients:</b> ${Object.values(ingrList).join(', ')}</p>
	               </div>
	              </li>`
 		$('ul.recipes').append(recipeTile);
		$(`#${recipe[i].id} .list-img`).css('background-image', `url(${recipe[i].image})`);
	    }
	});
    });

	const selectedDiets = [];
	const selectedIntolerances = [];
	$("#dropdownBtn").on("click", function() {
		$(".dropdown-menu").toggleClass("show");
	});

	$(document).click(function(e) {
		if (!$(e.target).closest('.dropdown').length) {
			$(".dropdown-menu").removeClass("show");
		}
	});

});
