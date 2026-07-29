
(function () {
  "use strict";

  var BATCH_SIZE = 5;

  document.addEventListener("DOMContentLoaded", function () {
    initViewMore();
    initTripTypeToggle();
    initAirportAutocomplete();
    initSearchLoader();
  });

  function initViewMore() {
    var viewMoreBtn = document.getElementById("vq-view-more");
    if (!viewMoreBtn) {
      return;
    }

    var list = document.getElementById("vq-flight-list");
    var countLabel = document.getElementById("vq-view-more-count");

    var getCards = function () {
      return Array.prototype.slice.call(list.querySelectorAll(".vq-flight-card"));
    };

    var updateCountLabel = function () {
      var remaining = getCards().filter(function (card) {
        return card.classList.contains("vq-hidden");
      }).length;

      if (remaining > 0) {
        countLabel.textContent = "(" + remaining + " more)";
      }
    };

    viewMoreBtn.addEventListener("click", function () {
      var hiddenCards = getCards().filter(function (card) {
        return card.classList.contains("vq-hidden");
      });

      var nextBatch = hiddenCards.slice(0, BATCH_SIZE);
      nextBatch.forEach(function (card) {
        card.classList.remove("vq-hidden");
      });

      var stillHidden = hiddenCards.length - nextBatch.length;

      if (stillHidden <= 0) {
        viewMoreBtn.parentElement.style.display = "none";
      } else {
        updateCountLabel();
      }

      // Keep focus manageable for keyboard users after content changes.
      if (nextBatch.length > 0) {
        nextBatch[0].setAttribute("tabindex", "-1");
        nextBatch[0].focus({ preventScroll: true });
      }
    });
  }


  function initTripTypeToggle() {
    var tripType = document.getElementById("vq-trip-type");
    var returnGroup = document.getElementById("vq-return-date-group");

    if (!tripType || !returnGroup) {
      return;
    }

    var syncReturnField = function () {
      var value = tripType.value.toLowerCase();
      var isOneWay = value.indexOf("one") !== -1 || value.indexOf("1") === 0;

      returnGroup.style.display = isOneWay ? "none" : "";

      var returnInput = returnGroup.querySelector("input, select");
      if (returnInput) {
        returnInput.disabled = isOneWay;

        if (isOneWay) {
          returnInput.value = "";
        }
      }
    };

    tripType.addEventListener("change", syncReturnField);
    syncReturnField();

  }

  function initAirportAutocomplete() {

    setupAirportSearch(
      "origin-input",
      "origin-suggestions"
    );

    setupAirportSearch(
      "destination-input",
      "destination-suggestions"
    );
  }

  async function fetchAirports(keyword) {

    const urls = [
        `/dashboard/airport/search?q=${encodeURIComponent(keyword)}`,
        `/airports/search?q=${encodeURIComponent(keyword)}`
    ];

    for (const url of urls) {

        try {

            const response = await fetch(url);

            if (response.ok) {
                return await response.json();
            }

        } catch (error) {
            console.log(`Failed: ${url}`);
        }
    }

    return [];
}

  function setupAirportSearch(inputId, suggestionId) {

    console.log("Initializing:", inputId);



    const input = document.getElementById(inputId);
    const suggestions = document.getElementById(suggestionId);

    if (!input || !suggestions) {
      return;
    }

    input.addEventListener("input", async function () {

      const keyword = input.value.trim();

      if (keyword.length < 1) {

        suggestions.style.display = "none";
        suggestions.innerHTML = "";

        return;
      }

      const airports = await fetchAirports(keyword);
      console.log("Airports received:", airports);

      suggestions.innerHTML = "";

      if (airports.length === 0) {

        suggestions.style.display = "none";

        return;
      }

      airports.forEach(function (airport) {

        const item = document.createElement("div");

        item.className = "airport-item";

        item.innerHTML = `
                <strong>${airport.city_name}</strong>
                (${airport.airport_code})
                <br>
                <small>${airport.airport_name}</small>
            `;

        item.addEventListener("click", function () {

          input.value = airport.airport_code;

          suggestions.innerHTML = "";
          suggestions.style.display = "none";
        });

        suggestions.appendChild(item);
      });

      suggestions.style.display = "block";
    });

    document.addEventListener("click", function (event) {

      if (
        !input.contains(event.target)
        &&
        !suggestions.contains(event.target)
      ) {

        suggestions.style.display = "none";
      }
    });
  }

  function initSearchLoader() {

    const form = document.querySelector("form");
    const button = document.getElementById("flight-search-btn");

    console.log(button);

    if (!form || !button) {
      return;
    }

    form.addEventListener("submit", function () {

      button.disabled = true;

      button.value = "Searching Flights...";

      button.style.opacity = "0.8";
      button.style.cursor = "wait";
    });
  }

})();