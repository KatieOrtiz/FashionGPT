// script.js

// Functionality for frontpage.html
document.addEventListener("DOMContentLoaded", function () {
  var button = document.getElementById("getStarted");
  button.addEventListener("click", function () {
    window.location.href = "emailVerification.html";
  });
  var button2 = document.getElementById("getStarted2");
  button2.addEventListener("click", function () {
    window.location.href = "emailVerification.html";
  });
});

// Functionality for emailverification.html
document.addEventListener("DOMContentLoaded", function () {
  var button = document.getElementById("backBtn");
  button.addEventListener("click", function () {
    window.location.href = "frontPage.html";
  });
});

// Functionality for homepage.html
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

// Functionality for continue button
document.addEventListener('DOMContentLoaded', function () {
  var continueBtn = document.getElementById('continue-btn1');
  if (continueBtn) { // Ensure the button exists before trying to add an event listener
    continueBtn.addEventListener('click', function() {
      window.location.href = 'registersize2.html';
    });
  }
});
// Functionality for continue button
document.addEventListener('DOMContentLoaded', function () {
  var continueBtn = document.getElementById('backBtnrs2');
  if (continueBtn) { // Ensure the button exists before trying to add an event listener
    continueBtn.addEventListener('click', function() {
      window.location.href = 'registerSize.html';
    });
  }
});
// Functionality for continue button
document.addEventListener('DOMContentLoaded', function () {
  var continueBtn = document.getElementById('backBtnrs1');
  if (continueBtn) { // Ensure the button exists before trying to add an event listener
    continueBtn.addEventListener('click', function() {
      window.location.href = 'register.html';
    });
  }
});
// Functionality for continue button
document.addEventListener('DOMContentLoaded', function () {
  var continueBtn = document.getElementById('backBtnev1');
  if (continueBtn) { // Ensure the button exists before trying to add an event listener
    continueBtn.addEventListener('click', function() {
      window.location.href = 'emailVerification.html';
    });
  }
});
//functionality for homepage next button
document.addEventListener('DOMContentLoaded', function() {
  // Global variable to store the IDs of clicked boxes
  var clickedBoxes = [];

  // Function to toggle box background color and update clickedBoxes array
  function toggleBox(box) {
    if (box.style.backgroundColor === 'gray' || box.style.backgroundColor === '') {
      box.style.backgroundColor = 'green';
      clickedBoxes.push(box.id); // Add clicked box ID to the array
    } else {
      box.style.backgroundColor = 'gray';
      // Remove clicked box ID from the array
      clickedBoxes = clickedBoxes.filter(function(id) {
        return id !== box.id;
      });
    }
  }

  // Event listener for box clicks
  const boxes = document.querySelectorAll('.box');
  boxes.forEach(box => {
    box.addEventListener('click', function() {
      toggleBox(this);
    });
  });

  // Event listener for the "Next" button
  var nextButton = document.getElementById('next-button');
  nextButton.addEventListener('click', function() {
    console.log(clickedBoxes);
    // You can send the IDs to server, store in localStorage, or perform any other action

    // Navigate to the next page
    window.location.href = 'nextPage.html'; // Replace 'next-page.html' with your actual next page URL
  });
});
