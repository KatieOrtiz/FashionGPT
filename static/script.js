//frontpage.html
document.addEventListener("DOMContentLoaded", function () {
  var button = document.getElementById("getStarted");
  button.addEventListener("click", function () {
    window.location.href = "login";
  });
  var button = document.getElementById("getStarted2");
  button.addEventListener("click", function () {
    window.location.href = "login";
  });
});

//emailverification.html
document.addEventListener("DOMContentLoaded", function () {
  var button = document.getElementById("backBtn");
  button.addEventListener("click", function () {
    window.location.href = "/";
  });
});

//homepage
document.addEventListener('DOMContentLoaded', function () {
    const coll = document.querySelectorAll('.collapsible');

    coll.forEach(function (item) {
        item.addEventListener('click', function () {
            this.classList.toggle('active');
            const content = this.nextElementSibling;
            if (content.style.display === 'block') {
                content.style.display = 'none';
            } else {
                content.style.display = 'block';
            }
        });
    });
});

document.addEventListener('DOMContentLoaded', function () {
  // Toggle active class for preference buttons
  document.querySelectorAll('.preference-button').forEach(button => {
      button.addEventListener('click', function () {
          this.classList.toggle('active');
      });
  });

  // Form submission handling
  document.getElementById('filters-form').addEventListener('submit', function (event) {
      event.preventDefault(); // Prevent the default form submission

      const formData = {
          priceRange: document.getElementById('price-range').value,
          outfitPreferences: [],
          seasonPreferences: [],
          stylePreferences: [],
      };

      // Collect active preferences
      document.querySelectorAll('#outfit-preferences .active').forEach(button => {
          formData.outfitPreferences.push(button.dataset.value);
      });
      document.querySelectorAll('#season-preferences .active').forEach(button => {
          formData.seasonPreferences.push(button.dataset.value);
      });
      document.querySelectorAll('#style-preferences .active').forEach(button => {
          formData.stylePreferences.push(button.dataset.value);
      });

      // Example: Send formData to server
      console.log(formData); // Replace this with the fetch API call

      // Reset active buttons if needed
      document.querySelectorAll('.preference-button.active').forEach(button => button.classList.remove('active'));
  });
});
