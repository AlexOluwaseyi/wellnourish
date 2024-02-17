$(document).ready(() => {

  // Clear all check boxes
  $('input[type="checkbox"]').each(function(){
      $(this).prop('checked', false);

  });

  // Get the popular recipes
  $.get('http://0.0.0.0:5001/api/v1/recipes', function (data) {
    const len = data.length;
    console.log(data);
    for (const recipe of data) {
      if (recipe.spoonacularScore >= 50) {
        const ingrList = [];
        for (const ingr of recipe.extendedIngredients) {
          ingrList.push(ingr.name);
        }

        $('.result-count h4').text(`Popular Recipes (${len})`);
        recipeTile = `<li id=${recipe.id}>
            <div class="list-img"></div>
            <div class="list-title">
            <h3>${recipe.title}</h3>
            <p><b>Ingredients:</b> ${Object.values(ingrList).join(', ')}</p>
            <p><b>Health Score:</b> ${recipe.healthScore}% </p>
            <p><b>Rating:</b> ${recipe.spoonacularScore}%</p>
            </div>
            </li>`;
        $('ul.recipes').append(recipeTile);
        $(`#${recipe.id} .list-img`).css('background-image', `url(${recipe.image})`);
      }
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

  let selectedFilters = {};
  $('.filter-options input[type="checkbox"]').on('change', function () {
      let filterOption = $(this);
      let filterId = filterOption.attr('id');
      let filterValue = filterOption.attr('value');
      if (filterOption.prop('checked')) {
	  selectedFilters[filterId] = filterValue
      }
      else {
	  delete selectedFilters[filterId];
      }

      console.log(Object.values(selectedFilters).join(', '));
  });

  // Returns search result
  $('.search-button').on('click', function () {
    $('.result-tiles ul').empty();
    const ingrs = $('.search-box input').val();
    $.get(`http://0.0.0.0:5001/api/v1/recipes/find_by_ingr/${ingrs}`, function (recipe) {
      const len = recipe.length;
      console.log(recipe);
      for (let i = 0; i < len; i++) {
        const ingrList = [];
        /* for (let ingr of recipe[i].usedIngredients) {
            ingrList.push(ingr.name);
        } */
        for (const ingr of recipe[i].missedIngredients) {
          ingrList.push(ingr.name);
        }
        $('.result-count h4').text(`Results (${len})`);
        recipeTile = `<li id=${recipe[i].id}>
        <div class="list-img"></div>
        <div class="list-title">
        <h3>${recipe[i].title}</h3>
        <p><b>Missing Ingredients:</b> ${Object.values(ingrList).join(', ')}</p>
        </div>
        </li>`;
        $('ul.recipes').append(recipeTile);
        $(`#${recipe[i].id} .list-img`).css('background-image', `url(${recipe[i].image})`);
      }
    });
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


  // Password Validation Code
  function validatePasswords () {
    const passwordInput = $('#password');
    const confirmPasswordInput = $('#confirmPassword');
    if (passwordInput.val() !== confirmPasswordInput.val()) {
      alert("Passwords don't match! Please re-enter.");
      confirmPasswordInput.focus(); // Set focus to confirm password field
      return false; // Prevent form submission
    }

    return true; // Allow form submission if passwords match
  }

  // Attaches the validatePasswords function to the form's submit event
  $('form').submit(function(event) {
    if (!validatePasswords()) {
      event.preventDefault(); // Prevent form submission if passwords don't match
    }
  });

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
