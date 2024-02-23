$(document).ready(() => {

  // Clear all check boxes
  $('input[type="checkbox"]').each(function(){
      $(this).prop('checked', false);

  });

  // Get the popular recipes
  $.get('http://0.0.0.0:5001/api/v1/recipes', function (data) {
    const len = data.length;
    for (const recipe of data) {
      if (recipe.spoonacularScore >= 50) {
        const ingrList = [];
        for (const ingr of recipe.extendedIngredients) {
          ingrList.push(ingr.name);
        }

        $('.result-count h4').text(`Popular Recipes (${len})`);
        recipeTile = `<a href="/recipes/${recipe.id}"><li id=${recipe.id}>
            <div class="list-img"></div>
            <div class="list-title">
            <h3>${recipe.title}</h3>
            <p><b>Ingredients:</b> ${Object.values(ingrList).join(', ')}</p>
            <p><b>Health Score:</b> ${recipe.healthScore}% </p>
            <p><b>Rating:</b> ${recipe.spoonacularScore}%</p>
            </div>
            </li></a>`;
        $('ul.recipes').append(recipeTile);
        $(`#${recipe.id} .list-img`).css('background-image', `url(${recipe.image})`);
      }
	$('.nav-button').addClass('hide_section');
    }
  });

  // Toggle Class when filter button is pressed
  $('.result-filter h4').on('click', function () {
      $('.filter-options').toggleClass('filter-options-show');
  });

  // Closes the filter menu when any area outside is clicked
    /**$('body').on('click', function(event) {
	  $(".filter-options").each(function() {
	      if ($(this).hasClass('filter-options-show')) {
		  $(this).removeClass('filter-options-show');
	      }
	  });
  });**/

  let selectedDiet = {};
  $('.filter-diet input[type="checkbox"]').on('change', function () {
      let filterOption = $(this);
      let filterId = filterOption.attr('id');
      let filterValue = filterOption.attr('value');
      if (filterOption.prop('checked')) {
	  selectedDiet[filterId] = filterValue
      }
      else {
	  delete selectedDiet[filterId];
      }

      /*console.log(Object.values(selectedFilters).join(', '));*/
  });

  let selectedIntolerance = {};
  $('.filter-intolerance input[type="checkbox"]').on('change', function () {
      let filterOption = $(this);
      let filterId = filterOption.attr('id');
      let filterValue = filterOption.attr('value');
      if (filterOption.prop('checked')) {
	  selectedIntolerance[filterId] = filterValue
      }
      else {
	  delete selectedIntolerance[filterId];
      }
  });

  // Returns search result
  $('.search-button').on('click', function () {
    $('.result-tiles ul').empty();
    const ingrs = $('.search-box input').val();
    const userDiet = $('#user_diets').text();
    const userIntol = $('#user_intolerances').text();
    let sUrl = `http://0.0.0.0:5001/api/v1/recipes/find_by_ingr/${ingrs}`;

    if (userDiet && userIntol) {
	sUrl = `http://0.0.0.0:5001/api/v1/recipes/find_by_ingr/${ingrs}/${userDiet}/${userIntol}/0`;
	console.log(sUrl);
    }
    else if (userDiet) {
	sUrl = `http://0.0.0.0:5001/api/v1/recipes/find_by_ingr/${ingrs}/d/${userDiet}/0`;
	console.log(sUrl);
    }
    else if (userIntol) {
	sUrl = `http://0.0.0.0:5001/api/v1/recipes/find_by_ingr/${ingrs}/t/${userIntol}/0`;
	console.log(sUrl);
    }

    $.get(sUrl, function (recipe) {
	//const len = recipe.totalResults;
	const len = recipe.results.length;
	console.log(recipe);
      for (let i = 0; i < recipe.number; i++) {
        const ingrList = [];
        /* for (let ingr of recipe[i].usedIngredients) {
            ingrList.push(ingr.name);
        } */
        for (const ingr of recipe.results[i].missedIngredients) {
          ingrList.push(ingr.name);
        }
        $('.result-count h4').text(`Results (${len})`);
        recipeTile = `<a href="/recipes/${recipe.results[i].id}"><li id=${recipe.results[i].id}>
        <div class="list-img"></div>
        <div class="list-title">
        <h3>${recipe.results[i].title}</h3>
        <p><b>Missing Ingredients:</b> ${Object.values(ingrList).join(', ')}</p>
        <p><b>Health Score:</b> ${recipe.results[i].healthScore}% </p>
        <p><b>Rating:</b> ${recipe.results[i].spoonacularScore}%</p>
        </div>
        </li></a>`;
        $('ul.recipes').append(recipeTile);
        $(`#${recipe.results[i].id} .list-img`).css('background-image', `url(${recipe.results[i].image})`);

	if (recipe.offset == 0) {
	    $('.nav-prev').addClass('hide_section');
	}
	else if (recipe.offset > recipe.totalResults) {
	    $('.nav-button').addClass('hide_section');
	}
      }
    });
  });

  // Filter search result
  $('.filter-button').on('click', function () {
    $('.result-tiles ul').empty();
      const ingrs = $('.search-box input').val();
      let searchUrl;

      console.log(selectedDiet);
      console.log(selectedIntolerance);

      if (Object.values(selectedDiet).length != 0 && Object.values(selectedIntolerance).length != 0) {
	  let sDiet = Object.values(selectedDiet).join(',');
	  let sIntol = Object.values(selectedIntolerance).join(',');
	  searchUrl = `http://0.0.0.0:5001/api/v1/recipes/find_by_ingr/${ingrs}/${sDiet}/${sIntol}/0`;
      }

      else if (Object.values(selectedDiet).length != 0) {
	  let sDiet = Object.values(selectedDiet).join(',');
	  searchUrl = `http://0.0.0.0:5001/api/v1/recipes/find_by_ingr/${ingrs}/d/${sDiet}/0`;
      }

      else if (Object.values(selectedIntolerance).length != 0) {
	  let sIntol = Object.values(selectedIntolerance).join(',');
	  searchUrl = `http://0.0.0.0:5001/api/v1/recipes/find_by_ingr/${ingrs}/i/${sIntol}/0`;
      }

      else {
	  searchUrl = `http://0.0.0.0:5001/api/v1/recipes/find_by_ingr/${ingrs}/0`;
      }

    console.log(searchUrl);
    $.get(searchUrl, function (recipe) {
	//const len = recipe.totalResults;
	const len = recipe.results.length;
	console.log(recipe);
      for (let i = 0; i < recipe.number; i++) {
        const ingrList = [];
        /* for (let ingr of recipe[i].usedIngredients) {
            ingrList.push(ingr.name);
        } */
        for (const ingr of recipe.results[i].missedIngredients) {
          ingrList.push(ingr.name);
        }
        $('.result-count h4').text(`Results (${len})`);
        recipeTile = `<a href="/recipes/${recipe.results[i].id}"><li id=${recipe.results[i].id}>
        <div class="list-img"></div>
        <div class="list-title">
        <h3>${recipe.results[i].title}</h3>
        <p><b>Missing Ingredients:</b> ${Object.values(ingrList).join(', ')}</p>
        <p><b>Health Score:</b> ${recipe.results[i].healthScore}% </p>
        <p><b>Rating:</b> ${recipe.results[i].spoonacularScore}%</p>
        </div>
        </li></a>`;
        $('ul.recipes').append(recipeTile);
        $(`#${recipe.results[i].id} .list-img`).css('background-image', `url(${recipe.results[i].image})`);

	if (recipe.offset == 0) {
	    $('.nav-prev').addClass('hide_section');
	}
	else if (recipe.offset > recipe.totalResults) {
	    $('.nav-button').addClass('hide_section');
	}
      }
    });
  });

  // Next/Prev search result
  $('.nav-button').on('click', function () {
      $('.nav-prev').removeClass('hide_section');
      $('.result-tiles ul').empty();
      const ingrs = $('.search-box input').val();
      let searchUrl;
      let offset;

      let btnNav = $(this);
      let btnNavId = btnNav.attr('id');
      let btnNavName = btnNav.attr('name');

      if (btnNavName === "next") {
	  offset = Number(btnNavId) + 19;
      }
      else {
	  offset = Number(btnNavId) - 19;
      }

      console.log(selectedDiet);
      console.log(selectedIntolerance);

      if (Object.values(selectedDiet).length != 0 && Object.values(selectedIntolerance).length != 0) {
	  let sDiet = Object.values(selectedDiet).join(',');
	  let sIntol = Object.values(selectedIntolerance).join(',');
	  searchUrl = `http://0.0.0.0:5001/api/v1/recipes/find_by_ingr/${ingrs}/${sDiet}/${sIntol}/${offset}`;
      }

      else if (Object.values(selectedDiet).length != 0) {
	  let sDiet = Object.values(selectedDiet).join(',');
	  searchUrl = `http://0.0.0.0:5001/api/v1/recipes/find_by_ingr/${ingrs}/d/${sDiet}/${offset}`;
      }

      else if (Object.values(selectedIntolerance).length != 0) {
	  let sIntol = Object.values(selectedIntolerance).join(',');
	  searchUrl = `http://0.0.0.0:5001/api/v1/recipes/find_by_ingr/${ingrs}/i/${sIntol}/${offset}`;
      }

      else {
	  searchUrl = `http://0.0.0.0:5001/api/v1/recipes/find_by_ingr/${ingrs}/${offset}`;
      }

    console.log(searchUrl);
    $.get(searchUrl, function (recipe) {
	const len = recipe.results.length;
	console.log(recipe);
      for (let i = 0; i < recipe.number; i++) {
        const ingrList = [];
        /* for (let ingr of recipe[i].usedIngredients) {
            ingrList.push(ingr.name);
        } */
        for (const ingr of recipe.results[i].missedIngredients) {
          ingrList.push(ingr.name);
        }
        $('.result-count h4').text(`Results (${len})`);
        recipeTile = `<a href="/recipes/${recipe.results[i].id}"><li id=${recipe.results[i].id}>
        <div class="list-img"></div>
        <div class="list-title">
        <h3>${recipe.results[i].title}</h3>
        <p><b>Missing Ingredients:</b> ${Object.values(ingrList).join(', ')}</p>
        <p><b>Health Score:</b> ${recipe.results[i].healthScore}% </p>
        <p><b>Rating:</b> ${recipe.results[i].spoonacularScore}%</p>
        </div>
        </li></a>`;
        $('ul.recipes').append(recipeTile);
        $(`#${recipe.results[i].id} .list-img`).css('background-image', `url(${recipe.results[i].image})`);

	if (recipe.totalResults <= recipe.offset) {
	   $('.nav-next').addClass('hide_section');
	}
	else if (recipe.offset > recipe.totalResults) {
	    $('.nav-button').addClass('hide_section');
	}
	else if (recipe.offset == 0) {
	    $('.nav-prev').addClass('hide_section');
	}
      }
    });

    $('.nav-button').attr('id', offset);
  });


  // Dropdown feature for profile completion
  $('.dropdown-container').each(function () {
    const $this = $(this); // Cache the jQuery object for the container
    const $label = $this.prev(); // Get the preceding label
    const $caret = $label.next().find('.caret-img'); // Select the caret image

    // Close dropdown when clicking outside
    $(document).click(function (event) {
      if (!$this.is(event.target) && !$this.has(event.target).length &&
        !$label.is(event.target) && !$label.has(event.target).length) {
        $this.hide();
        $caret.css('transform', 'rotate(0deg)'); // Reset rotation when closing
      }
    });

    // Toggle dropdown and update caret rotation
    $label.click(function () {
      $this.toggle();
      $caret.css('transform', $this.is(':visible') ? 'rotate(180deg)' : 'rotate(0deg)');
    });
  });


  // Password Validation Code on registration
  function validatePasswords () {
    const passwordInput = $('#password');
    const confirmPasswordInput = $('#confirmPassword');
    if (passwordInput.val() !== confirmPasswordInput.val()) {
      alert("Passwords don't match! Please re-enter.");
      confirmPasswordInput.focus(); // Set focus to confirm password field
      return false; // Prevent form submission
    }

    setTimeout(function() {
      $('.alert').alert('close');
    }, 5000);

    return true; // Allow form submission if passwords match
  }

  // Attaches the validatePasswords function to the form's submit event
  $('form').submit(function(event) {
    if (!validatePasswords()) {
      event.preventDefault(); // Prevent form submission if passwords don't match
    }
  });

  $("#flash-message").show().delay(3000).fadeOut(400, "linear", function() {
    // Check if the flash message is still visible
    if ($(this).is(":visible")) {
        // Flash message is still visible, prevent form submission
        $("form").submit(function(event) {
            event.preventDefault(); // Prevent the default form submission
        });
    }
  });

  // $("#flash-message").show().delay(3000).fadeOut(400, "linear", function() {
  //   // Flash message is still visible, prevent form submission
  //   $("form").submit(function(event) {
  //       event.preventDefault(); // Prevent the default form submission
  //   });
  // });

  // $("#flash-message").show().delay(3000).fadeOut(400, "linear")
  
  const selectedDiets = {};
  const selectedIntolerances = {};

  // Collects checked items from Diets dropdown
  $('#diet-dropdown input[type="checkbox"]').on('click', function () {
    const dietId = $(this).data('id');
    const dietName = $(this).data('value');
    if (Object.prototype.hasOwnProperty.call(selectedDiets, dietId)) {
      delete selectedDiets[dietId];
    } else {
      selectedDiets[dietId] = dietName;
    }
    const dietsString = Object.values(selectedDiets).join(', ');
    $('.diet-p').text(Object.values(selectedDiets).join(', '));
    $('#diets-string').val(dietsString);
  });

  // Collects checked items from Intolerances dropdown
  $('#intolerance-dropdown input[type="checkbox"]').on('click', function () {
    const intoleranceId = $(this).data('id');
    const intoleranceName = $(this).data('value');
    if (Object.prototype.hasOwnProperty.call(selectedIntolerances, intoleranceId)) {
      delete selectedIntolerances[intoleranceId];
    } else {
      selectedIntolerances[intoleranceId] = intoleranceName;
    }
    const intolerancesString = Object.values(selectedIntolerances).join(', ');
    $('.intolerance-p').text(Object.values(selectedIntolerances).join(', '));
    $('#intolerances-string').val(intolerancesString);
  });

});
