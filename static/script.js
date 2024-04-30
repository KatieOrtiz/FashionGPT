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
    window.location.href = "frontPage";
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
// Functionality for continue button
document.addEventListener('DOMContentLoaded', function () {
  var continueBtn = document.getElementById('continue-btn1');
  if (continueBtn) { // Ensure the button exists before trying to add an event listener
    continueBtn.addEventListener('click', function() {
      window.location.href = 'registersize2';
    });
  }
});
// Functionality for continue button
document.addEventListener('DOMContentLoaded', function () {
  var continueBtn = document.getElementById('backBtnrs2');
  if (continueBtn) { // Ensure the button exists before trying to add an event listener
    continueBtn.addEventListener('click', function() {
      window.location.href = 'registerSize';
    });
  }
});
// Functionality for continue button
document.addEventListener('DOMContentLoaded', function () {
  var continueBtn = document.getElementById('backBtnrs1');
  if (continueBtn) { // Ensure the button exists before trying to add an event listener
    continueBtn.addEventListener('click', function() {
      window.location.href = 'register';
    });
  }
});
// Functionality for continue button
document.addEventListener('DOMContentLoaded', function () {
  var continueBtn = document.getElementById('backBtnev1');
  if (continueBtn) { // Ensure the button exists before trying to add an event listener
    continueBtn.addEventListener('click', function() {
      window.location.href = 'emailVerification';
    });
  }
});