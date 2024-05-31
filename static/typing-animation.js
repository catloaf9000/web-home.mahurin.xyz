document.addEventListener("DOMContentLoaded", function() {
    const textElement = document.getElementById("typing-text");
    const resultElements = document.querySelectorAll(".terminal__result");
    const resultDelay = parseInt(textElement.getAttribute("data-delay")) || 200; // Delay in milliseconds for each result element to appear

    if (textElement) {
        const text = textElement.textContent;
        const speed = parseInt(textElement.getAttribute("data-speed")) || 5;
        textElement.textContent = ""; // Clear the initial text
        let index = 0;
        const cursorSymbol = "█";

        function type() {
            if (index < text.length) {
                textElement.textContent = text.slice(0, index) + cursorSymbol;
                index++;
                setTimeout(type, 100 / speed); // Adjust the speed of typing here
            } else {
                textElement.textContent = text;
                showResults();
                hideInputs();
            }
        }

        function showResults() {
            resultElements.forEach((element, i) => {
                setTimeout(() => {
                    element.style.display = "block"; // Show the element
                }, resultDelay * (i + 1));
            });
        }

        function hideInputs() {
            const elements = document.querySelectorAll('.terminal_hide');
            elements.forEach(element => {
                setTimeout(() => {
                    element.style.display = 'none';
                }, resultDelay) 
            });
        }

        // Initially hide all result elements
        resultElements.forEach(element => {
            element.style.display = "none";
        });

        type();
    }
});
