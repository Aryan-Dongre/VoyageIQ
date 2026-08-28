(function () {
    "use strict";

    console.log("VoyageIQ Dashboard JS loaded");

    document.addEventListener("DOMContentLoaded", function () {

        console.log("Dashboard DOM loaded");

        /*
         * Support both possible IDs:
         *
         * origin
         * origin-input
         *
         * destination
         * destination-input
         */

        const originInput =
            document.getElementById("origin") ||
            document.getElementById("origin-input");

        const destinationInput =
            document.getElementById("destination") ||
            document.getElementById("destination-input");


        console.log("Origin input:", originInput);
        console.log("Destination input:", destinationInput);


        if (!originInput) {
            console.error("Origin input not found");
        }

        if (!destinationInput) {
            console.error("Destination input not found");
        }


        setupAirportSearch(
            originInput,
            "origin-suggestions"
        );

        setupAirportSearch(
            destinationInput,
            "destination-suggestions"
        );


        /*
         * =====================================================
         * AIRPORT SEARCH
         * =====================================================
         */

        function setupAirportSearch(input, suggestionId) {

            if (!input) {
                return;
            }


            let suggestionBox = document.getElementById(suggestionId);

            let debounceTimer = null;

            let controller = null;


            /*
             * If the suggestion box does not already exist
             * in HTML, create it.
             */

            if (!suggestionBox) {

                suggestionBox = document.createElement("div");

                suggestionBox.id = suggestionId;

                suggestionBox.className =
                    "airport-suggestions";

                input.parentElement.style.position =
                    "relative";

                input.parentElement.appendChild(
                    suggestionBox
                );
            }


            /*
             * =================================================
             * INPUT
             * =================================================
             */

            input.addEventListener("input", function () {

                const keyword =
                    input.value.trim();


                /*
                 * If user starts typing manually again,
                 * remove the previously selected airport code.
                 */

                delete input.dataset.airportCode;


                clearTimeout(debounceTimer);


                if (controller) {

                    controller.abort();

                    controller = null;
                }


                suggestionBox.innerHTML = "";

                suggestionBox.style.display = "none";


                /*
                 * Don't search for less than 2 characters
                 */

                if (keyword.length < 2) {

                    return;
                }


                /*
                 * Wait 250ms before sending request
                 */

                debounceTimer = setTimeout(
                    async function () {

                        controller =
                            new AbortController();


                        try {

                            console.log(
                                "Searching airport:",
                                keyword
                            );


                            const response =
                                await fetch(
                                    `/dashboard/airport/search?q=${encodeURIComponent(keyword)}`,
                                    {
                                        signal:
                                            controller.signal
                                    }
                                );


                            console.log(
                                "Airport response:",
                                response.status
                            );


                            if (!response.ok) {

                                console.error(
                                    "Airport search failed:",
                                    response.status
                                );

                                return;
                            }


                            const airports =
                                await response.json();


                            console.log(
                                "Airports received:",
                                airports
                            );


                            /*
                             * Make sure the user has not
                             * changed the input while the
                             * request was running.
                             */

                            if (
                                input.value.trim() !==
                                keyword
                            ) {

                                return;
                            }


                            if (
                                !airports ||
                                airports.length === 0
                            ) {

                                return;
                            }


                            createSuggestions(
                                input,
                                suggestionBox,
                                airports
                            );


                        } catch (error) {

                            if (
                                error.name !==
                                "AbortError"
                            ) {

                                console.error(
                                    "Airport autocomplete error:",
                                    error
                                );

                            }

                        }

                    },
                    250
                );

            });


            /*
             * =================================================
             * CREATE SUGGESTIONS
             * =================================================
             */

            function createSuggestions(
                input,
                suggestionBox,
                airports
            ) {

                suggestionBox.innerHTML = "";


                airports
                    .slice(0, 6)
                    .forEach(function (airport) {

                        const item =
                            document.createElement("div");


                        item.className =
                            "airport-suggestion-item";


                        /*
                         * EXACTLY THE SAME DISPLAY
                         * AS PUBLIC FLIGHT PAGE
                         */

                        item.innerHTML = `
                            <div class="airport-city">
                                ${airport.city_name}
                                <span>
                                    (${airport.airport_code})
                                </span>
                            </div>

                            <div class="airport-name">
                                ${airport.airport_name}
                            </div>
                        `;


                        /*
                         * =================================================
                         * WHEN USER CLICKS SUGGESTION
                         * =================================================
                         *
                         * Visible:
                         *
                         * Mumbai (BOM)
                         *
                         * Stored code:
                         *
                         * BOM
                         */

                        item.addEventListener(
                            "click",
                            function () {

                                input.value =
                                    `${airport.city_name} (${airport.airport_code})`;


                                input.dataset.airportCode =
                                    airport.airport_code;


                                console.log(
                                    "Selected airport:",
                                    airport.airport_code
                                );


                                suggestionBox.innerHTML =
                                    "";

                                suggestionBox.style.display =
                                    "none";

                            }
                        );


                        suggestionBox.appendChild(
                            item
                        );

                    });


                suggestionBox.style.display =
                    "block";

            }


            /*
             * =================================================
             * CLICK OUTSIDE
             * =================================================
             */

            document.addEventListener(
                "click",
                function (event) {

                    if (
                        event.target !== input &&
                        !suggestionBox.contains(
                            event.target
                        )
                    ) {

                        suggestionBox.style.display =
                            "none";

                    }

                }
            );

        }


        /*
         * =====================================================
         * FORM SUBMISSION
         * =====================================================
         *
         * Convert:
         *
         * Mumbai (BOM)
         *
         * into:
         *
         * BOM
         *
         * before Flask receives the form.
         */

        const form =
            document.querySelector("form");


        if (form) {

            form.addEventListener(
                "submit",
                function () {

                    console.log(
                        "Submitting dashboard form"
                    );


                    /*
                     * ORIGIN
                     */

                    if (
                        originInput &&
                        originInput.dataset.airportCode
                    ) {

                        originInput.value =
                            originInput.dataset.airportCode;

                    }


                    /*
                     * DESTINATION
                     */

                    if (
                        destinationInput &&
                        destinationInput.dataset.airportCode
                    ) {

                        destinationInput.value =
                            destinationInput.dataset.airportCode;

                    }


                    console.log(
                        "Origin submitted:",
                        originInput
                            ? originInput.value
                            : null
                    );


                    console.log(
                        "Destination submitted:",
                        destinationInput
                            ? destinationInput.value
                            : null
                    );

                }
            );

        }

    });

})();