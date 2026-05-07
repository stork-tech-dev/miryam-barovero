(function () {
  var header = document.getElementById("siteHeader");
  var hamburger = document.getElementById("navToggle");
  var navMain = document.getElementById("navMain");

  function onScroll() {
    if (!header) return;
    header.classList.toggle("is-scrolled", window.scrollY > 24);
  }

  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  if (hamburger && navMain) {
    hamburger.addEventListener("click", function () {
      var open = navMain.classList.toggle("is-open");
      hamburger.classList.toggle("is-open", open);
      hamburger.setAttribute("aria-expanded", open ? "true" : "false");
    });

    navMain.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        navMain.classList.remove("is-open");
        hamburger.classList.remove("is-open");
        hamburger.setAttribute("aria-expanded", "false");
      });
    });
  }
})();
