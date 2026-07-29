
document.addEventListener("DOMContentLoaded", function () {
  initDestinationAutocomplete();
  initViewMore();
});


/* 1. Destination autocomplete */


function initDestinationAutocomplete() {
  const input = document.getElementById("destination-input");
  const suggestionsBox = document.getElementById("destination-suggestions");

  if (!input || !suggestionsBox) return;

  let debounceTimer = null;

  input.addEventListener("input", function () {
    const query = input.value.trim();

    clearTimeout(debounceTimer);

    if (query.length < 2) {
      hideSuggestions();
      return;
    }

    // Debounce so we don't spam suggestion lookups while typing.
    debounceTimer = setTimeout(function () {
      // Hook point: the shared destination-suggestion service should
      // populate #destination-suggestions here, e.g.:
      // fetchDestinationSuggestions(query).then(renderSuggestions);
      renderSuggestions(getPlaceholderSuggestions(query));
    }, 200);
  });

  document.addEventListener("click", function (e) {
    if (!suggestionsBox.contains(e.target) && e.target !== input) {
      hideSuggestions();
    }
  });

  input.addEventListener("keydown", function (e) {
    if (e.key === "Escape") hideSuggestions();
  });

  function renderSuggestions(items) {
    suggestionsBox.innerHTML = "";

    if (!items || items.length === 0) {
      hideSuggestions();
      return;
    }

    items.forEach(function (item) {
      const el = document.createElement("div");
      el.className = "vq-suggestion-item";
      el.textContent = item;
      el.addEventListener("click", function () {
        input.value = item;
        hideSuggestions();
        input.focus();
      });
      suggestionsBox.appendChild(el);
    });

    showSuggestions();
  }

  function showSuggestions() {
    suggestionsBox.classList.remove("vq-hidden");
  }

  function hideSuggestions() {
    suggestionsBox.classList.add("vq-hidden");
  }

  // Placeholder only — replace with real destination data source.
  function getPlaceholderSuggestions(query) {
    const sample = [
      "Goa, India",
      "Dubai, UAE",
      "Paris, France",
      "Bali, Indonesia",
      "New York, USA",
      "Singapore",
      "Bangkok, Thailand",
      "Rome, Italy",
    ];
    return sample.filter(function (place) {
      return place.toLowerCase().includes(query.toLowerCase());
    });
  }
}





/* 2. View More hotels                                                    */

function initViewMore() {
  const viewMoreBtn = document.getElementById("vq-view-more");
  const hotelList = document.getElementById("vq-hotel-list");

  if (!viewMoreBtn || !hotelList) return;

  viewMoreBtn.addEventListener("click", function () {
    const hiddenCards = hotelList.querySelectorAll(".vq-hotel-card.vq-hidden");

    hiddenCards.forEach(function (card) {
      card.classList.remove("vq-hidden");
    });

    viewMoreBtn.classList.add("vq-hidden");
  });
}