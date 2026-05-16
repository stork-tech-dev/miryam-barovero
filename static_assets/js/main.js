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

  window.initSiteToast = function initSiteToast() {
    var toastOverlay = document.getElementById("siteToastOverlay");
    if (!toastOverlay) return;

    var autoCloseTimer = null;

    function onEscape(event) {
      if (event.key === "Escape") {
        dismissToast();
      }
    }

    function dismissToast() {
      var redirectUrl = toastOverlay.getAttribute("data-redirect-on-close");
      if (autoCloseTimer) {
        window.clearTimeout(autoCloseTimer);
        autoCloseTimer = null;
      }
      document.removeEventListener("keydown", onEscape);
      toastOverlay.classList.remove("is-visible");
      toastOverlay.style.pointerEvents = "none";
      window.setTimeout(function () {
        if (toastOverlay.parentNode) {
          toastOverlay.parentNode.removeChild(toastOverlay);
        }
        if (redirectUrl) {
          window.location.href = redirectUrl;
        }
      }, 280);
    }

    toastOverlay.addEventListener("click", function (event) {
      if (event.target.closest("[data-dismiss='toast']")) {
        event.preventDefault();
        event.stopPropagation();
        dismissToast();
        return;
      }
      if (event.target === toastOverlay) {
        dismissToast();
      }
    });

    document.addEventListener("keydown", onEscape);

    autoCloseTimer = window.setTimeout(dismissToast, 8000);
  }

  window.initSiteToast();

  if (window.location.hash === "#resultado") {
    var resultEl = document.getElementById("resultado");
    if (resultEl) {
      resultEl.focus({ preventScroll: true });
      resultEl.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  }
})();
