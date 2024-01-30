//frontpage.html
document.addEventListener("DOMContentLoaded", function () {
  var button = document.getElementById("getStarted");
  button.addEventListener("click", function () {
    window.location.href = "emailVerification";
  });
  var button = document.getElementById("getStarted2");
  button.addEventListener("click", function () {
    window.location.href = "emailVerification";
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

