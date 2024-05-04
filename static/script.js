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

//login.html
document.addEventListener("DOMContentLoaded", function () {
  var button = document.getElementById("backBtn");
  button.addEventListener("click", function () {
    window.location.href = "index";
  });
});
//register.html
document.addEventListener("DOMContentLoaded", function () {
  var button = document.getElementById("backBtn1");
  button.addEventListener("click", function () {
    window.location.href = "login";
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
document.addEventListener("DOMContentLoaded", function() {
  // Code to execute after DOM content is fully loaded
  document.getElementById('homebutton').addEventListener('click', function() {
    window.location.href = 'dashboard';
  });

  document.getElementById('likebutton').addEventListener('click', function() {
    window.location.href = 'favorites';
  });

  document.getElementById('settingbutton').addEventListener('click', function() {
    window.location.href = 'userSettings';
  });
});
//RegisterSize 
document.addEventListener("DOMContentLoaded", (event) => {
  // Function to hide all sections
  function hideAllSections() {
    const sections = document.querySelectorAll(".verification");
    sections.forEach((section) => {
      section.classList.add("hidden");
      section.classList.remove("fade-in");
    });
  }

  // Initially hide all sections
  hideAllSections();

  // Show the first section by default
  const firstSection = document.getElementById("section1");
  if (firstSection) {
    firstSection.classList.remove("hidden");
  }

  // Function to show the next section
  window.showSection = function (sectionNumber) {
    hideAllSections();
    const currentSection = document.querySelector(".verification:not(.hidden)");
    const nextSection = document.getElementById(`section${sectionNumber}`);
    if (currentSection && nextSection) {
      currentSection.classList.add("hidden");
      currentSection.classList.remove("fade-in");
      nextSection.classList.remove("hidden");
    }
  };

  // Function to go back to the previous section
  function goBack(sectionNumber) {
    const currentSection = document.getElementById(`section${sectionNumber}`);
    if (currentSection) {
      currentSection.classList.add("hidden");
      const previousSectionNumber = sectionNumber - 1;
      const previousSection = document.getElementById(`section${previousSectionNumber}`);
      if (previousSection) {
        previousSection.classList.remove("hidden");
      }
    }
  }

  // Event listeners for back buttons
  document.getElementById("back2sec1").addEventListener("click", () => {
    goBack(2);
  });
  document.getElementById("back2sec2").addEventListener("click", () => {
    goBack(3);
  });

  document.getElementById("back2sec3").addEventListener("click", () => {
    goBack(4);
  });

  document.getElementById("back2sec4").addEventListener("click", () => {
    goBack(5);
  });
});

