$(document).ready(function (){
    let recipe_id = $('.hidden-text').text()
    $.get(`http://0.0.0.0:5001/api/v1/recipes/${recipe_id}`, function (recipe) {
	$('.recipe_title p').text(recipe.title);

	$('.recipe_img').css('background-image', `url(${recipe.image})`);

	$('.recipe_img_credits p span').html(`: <a href="${recipe.sourceUrl}">${recipe.creditsText}</a>`);

	$('.recipe_summary p').html(recipe.summary);


	for (const ingr of recipe.extendedIngredients) {
	    let ingrGrid = `<div class="ing_card" id="${ingr.id}">
	                       <div class="ing_amount_metric">${ingr.amount} ${ingr.unit}</div>
	                       <div class="ing_image"></div>
	                       <div class="ing_name">${ingr.nameClean}</div>
	                    </div>`;
	    let ingrList = `<div class="ing_slot" id="${ingr.id}">
	                       <div class="ing_slot_image"></div>
                               <div class="ing_slot_amount_metric">${ingr.amount} ${ingr.unit}</div>
	                       <div class="ing_slot_name">${ingr.nameClean}</div>
	                    </div>`;
	    $('.ing_grid').append(ingrGrid);
	    $('.ing_list').append(ingrList);
	    let image_url = `https://spoonacular.com/cdn/ingredients_100x100/${ingr.image}`
            $(`#${ingr.id} .ing_image`).css('background-image', `url("${image_url}")`);
	    $(`#${ingr.id} .ing_slot_image`).css('background-image', `url("${image_url}")`);
	}

	if (recipe.analyzedInstructions.length === 0){
	    $('.recipe_instructions p').html(`Read the detailed instructions <a href="${recipe.sourceUrl}">here.</a>`)
	    $('.detailed_instructions ol').empty();
	}
	else {
	    $('.recipe_instructions p').html(`Read the detailed instructions <a href="${recipe.sourceUrl}">here.</a>`)
	    for (const inst of recipe.analyzedInstructions[0].steps) {
		let instList = `<li>${inst.step}</li>`;
		$('.detailed_instructions ol').append(instList);
	    }
	}
    });

    $('#ing_list').addClass('hide_section');

    $('#grid_dis').on('click', function () {
	$('#ing_list').addClass('hide_section');
	$('#ing_grid').removeClass('hide_section');
    });

    $('#list_dis').on('click', function () {
	$('#ing_grid').addClass('hide_section');
	$('#ing_list').removeClass('hide_section');
    });

    $('#eq_list').addClass('hide_section');

    $('#e_grid_dis').on('click', function () {
	$('#eq_list').addClass('hide_section');
	$('#eq_grid').removeClass('hide_section');
    });

    $('#e_list_dis').on('click', function () {
	$('#eq_grid').addClass('hide_section');
	$('#eq_list').removeClass('hide_section');
    });
});
