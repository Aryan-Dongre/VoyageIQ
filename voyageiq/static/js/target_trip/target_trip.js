
async function setupAirportAutocomplete(
    inputId,
    suggestionId
) {

    const input = document.getElementById(inputId);

    const suggestions = document.getElementById(suggestionId);

    input.addEventListener("input", async function () {

        const keyword = input.value.trim();

        if (keyword.length < 2) {
            suggestions.style.display = "none";
            suggestions.innerHTML = "";
            return;
        }

        const response = await fetch(
            `/flight/airports/search?q=${encodeURIComponent(keyword)}`
        );

        const airports = await response.json();

        suggestions.innerHTML = "";

        if (airports.length === 0) {
            suggestions.style.display = "none";
            return;
        }

        airports.forEach((airport) => {

            const item = document.createElement("div");

            item.className = "airport-item";

            item.innerHTML = `
                <div class="airport-code">
                    ${airport.airport_code}
                </div>

                <div class="airport-name">
                    ${airport.city_name}
                    -
                    ${airport.airport_name}
                </div>
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
            !input.contains(event.target) &&
            !suggestions.contains(event.target)
        ) {

            suggestions.style.display = "none";

        }
    });

}

setupAirportAutocomplete(
    "origin-input",
    "origin-suggestions"
);

setupAirportAutocomplete(
    "destination-input",
    "destination-suggestions"
);

