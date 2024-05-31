document.addEventListener("DOMContentLoaded", () => {
    const textElement = document.getElementById("typing-text");
    const resultElements = document.querySelectorAll(".terminal__result");
    const inputElements = document.querySelectorAll('.terminal_hide');

    if (!textElement) return;

    const text = textElement.textContent;
    const typingSpeed = parseInt(textElement.getAttribute("data-speed"), 10) || 5;
    const resultDelay = parseInt(textElement.getAttribute("data-delay"), 10) || 200; // Delay for each result element

    // Clear initial content
    textElement.textContent = "";
    resultElements.forEach(el => el.style.display = "none");

    let index = 0;
    const cursorSymbol = "█";

    const type = () => {
        if (index < text.length) {
            textElement.textContent = text.slice(0, index) + cursorSymbol;
            index++;
            setTimeout(type, 100 / typingSpeed);
        } else {
            textElement.textContent = text; // Remove cursor after typing
            displayResults();
            hideInputs();
        }
    };

    const displayResults = () => {
        resultElements.forEach((element, i) => {
            setTimeout(() => {
                element.style.display = "block";
            }, resultDelay * (i + 1));
        });
    };

    const hideInputs = () => {
        inputElements.forEach(element => {
            setTimeout(() => {
                element.style.display = 'none';
            }, resultDelay * inputElements.length); // Hide inputs after all results are displayed
        });
    };

    type();
});
