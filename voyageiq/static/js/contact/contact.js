document.addEventListener("DOMContentLoaded", function () {
    initCategoryCards();
    initCharCounter();
    initFormSubmit();
    initSmoothScroll();
});

/* ==================================================
   CATEGORY CARD SELECTION
================================================== */

function initCategoryCards() {

    const cards = document.querySelectorAll(".contact-card");
    const categorySelect = document.getElementById("category");

    if (!cards.length) return;

    cards.forEach((card) => {

        card.addEventListener("click", () => {

            cards.forEach((c) => {
                c.classList.remove("is-selected");
            });

            card.classList.add("is-selected");

            const category = card.dataset.category;

            if (categorySelect) {
                categorySelect.value = category;
            }

            const formSection = document.querySelector(".contact-form-wrapper");

            if (formSection) {
                formSection.scrollIntoView({
                    behavior: "smooth",
                    block: "center"
                });
            }
        });

    });
}

/* ==================================================
   CHARACTER COUNTER
================================================== */

function initCharCounter() {

    const messageField = document.getElementById("message");
    const counter = document.getElementById("charCounter");

    if (!messageField || !counter) return;

    const maxLength =
        parseInt(messageField.getAttribute("maxlength")) || 1000;

    function updateCounter() {

        const currentLength = messageField.value.length;

        counter.textContent =
            `${currentLength} / ${maxLength}`;

        counter.classList.remove(
            "is-near-limit",
            "is-limit-reached"
        );

        if (currentLength >= maxLength) {

            counter.classList.add("is-limit-reached");

        } else if (currentLength >= maxLength * 0.9) {

            counter.classList.add("is-near-limit");
        }
    }

    updateCounter();

    messageField.addEventListener("input", updateCounter);
}

/* ==================================================
   FORM SUBMISSION
================================================== */

function initFormSubmit() {

    const form = document.getElementById("contactForm");
    const submitBtn = document.getElementById("submitBtn");

    if (!submitBtn) return;

    const submitText =
        submitBtn.querySelector(".contact-form__submit-text");

    /* ------------------------------------------
       SUCCESS STATE AFTER PAGE RELOAD
    ------------------------------------------ */

    if (window.contactSuccess) {

        submitBtn.classList.remove("is-loading");

        submitBtn.style.backgroundColor = "#16a34a";
        submitBtn.style.borderColor = "#16a34a";
        submitBtn.style.color = "#ffffff";

        submitBtn.disabled = true;

        if (submitText) {
            submitText.textContent = "✓ Message Sent";
        }

        setTimeout(() => {

            submitBtn.style.backgroundColor = "";
            submitBtn.style.borderColor = "";
            submitBtn.style.color = "";

            submitBtn.disabled = false;

            if (submitText) {
                submitText.textContent = "Send Message";
            }

        }, 5000);

        return;
    }

    /* ------------------------------------------
       LOADING STATE BEFORE SUBMIT
    ------------------------------------------ */

    if (!form) return;

    form.addEventListener("submit", function () {

        submitBtn.disabled = true;

        submitBtn.classList.add("is-loading");

        if (submitText) {
            submitText.textContent = "Sending...";
        }
    });
}

/* ==================================================
   SMOOTH SCROLL
================================================== */

function initSmoothScroll() {

    document
        .querySelectorAll('a[href^="#"]')
        .forEach((anchor) => {

            anchor.addEventListener("click", function (e) {

                const targetId =
                    this.getAttribute("href").substring(1);

                const target =
                    document.getElementById(targetId);

                if (!target) return;

                e.preventDefault();

                target.scrollIntoView({
                    behavior: "smooth",
                    block: "start"
                });
            });

        });
}