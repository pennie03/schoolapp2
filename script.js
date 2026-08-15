/* =================================
   STUDYHUB - INTERACTIONS
   ================================= */

// Smooth scrolling for internal links
document.addEventListener("click", function (event) {

    const target = event.target.closest("[data-scroll]");

    if (!target) return;

    const section = document.querySelector(
        target.getAttribute("data-scroll")
    );

    if (section) {
        section.scrollIntoView({
            behavior: "smooth"
        });
    }
});


// Add a subtle loading state to buttons
document.addEventListener("click", function (event) {

    const button = event.target.closest("button");

    if (!button) return;

    button.classList.add("button-clicked");

    setTimeout(() => {
        button.classList.remove("button-clicked");
    }, 300);

});


// Simple typing animation helper
function typeText(element, text, speed = 25) {

    if (!element) return;

    element.textContent = "";

    let index = 0;

    function type() {

        if (index < text.length) {

            element.textContent += text.charAt(index);

            index++;

            setTimeout(type, speed);
        }
    }

    type();
}

