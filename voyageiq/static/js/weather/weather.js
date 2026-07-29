
document.addEventListener("DOMContentLoaded", function () {
  initSearchLoader();
  initSmoothScrollToResults();
  initForecastCardHover();
});

/* ---------------------------------------------------------
   SEARCH LOADER
   Disable the submit button and show a loading state while
   the weather search request is in flight.
   --------------------------------------------------------- */
function initSearchLoader() {
  var form = document.getElementById("vq-weather-search-form");
  var submitBtn = document.getElementById("vq-search-submit");

  if (!form || !submitBtn) return;

  form.addEventListener("submit", function (event) {
    var destinationInput = form.querySelector(".vq-input");

    if (destinationInput && !destinationInput.value.trim()) {
      return;
    }

    submitBtn.disabled = true;
    submitBtn.dataset.originalText = submitBtn.value || submitBtn.textContent;

    if (submitBtn.tagName === "INPUT") {
      submitBtn.value = "Loading weather...";
    } else {
      submitBtn.textContent = "Loading weather...";
    }
  });
}

/* ---------------------------------------------------------
   SMOOTH SCROLL
   After results render on the page, smoothly scroll the
   Weather Results section into view.
   --------------------------------------------------------- */
function initSmoothScrollToResults() {
  var resultsSection = document.getElementById("vq-weather-results");
  if (!resultsSection) return;

  var hasResults = resultsSection.querySelector(".vq-weather-current");
  if (!hasResults) return;

  window.requestAnimationFrame(function () {
    resultsSection.scrollIntoView({ behavior: "smooth", block: "start" });
  });
}

/* ---------------------------------------------------------
   FORECAST CARD HOVER ANIMATION
   Lightweight interaction only — toggles a class so the
   card lift/shadow defined in CSS can be triggered on touch
   devices too (which don't fire native :hover reliably).
   --------------------------------------------------------- */
function initForecastCardHover() {
  var forecastCards = document.querySelectorAll(".vq-forecast-card");
  if (!forecastCards.length) return;

  forecastCards.forEach(function (card) {
    card.addEventListener("mouseenter", function () {
      card.classList.add("is-active");
    });

    card.addEventListener("mouseleave", function () {
      card.classList.remove("is-active");
    });

    card.addEventListener("touchstart", function () {
      forecastCards.forEach(function (c) {
        if (c !== card) c.classList.remove("is-active");
      });
      card.classList.add("is-active");
    }, { passive: true });
  });
}