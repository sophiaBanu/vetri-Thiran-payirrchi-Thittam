const task = document.getElementById("task");
const inputText = document.getElementById("inputText");

const generateButton = document.getElementById("generateButton");
const clearButton = document.getElementById("clearButton");

const statusBox = document.getElementById("status");

const resultSection = document.getElementById("resultSection");
const resultBox = document.getElementById("result");


const endpoints = {
    qa: "/qa",
    explain: "/explain",
    quiz: "/quiz",
    summarize: "/summarize",
    learn: "/learn/recommendations"
};


function escapeHtml(value) {

    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}


function renderResult(taskName, data) {

    // Quiz result
    if (taskName === "quiz" && Array.isArray(data)) {

        resultBox.innerHTML = data.map((item, index) => {

            const options = Array.isArray(item.options)
                ? item.options.map(option => `
                    <div class="option">
                        ${escapeHtml(option)}
                    </div>
                `).join("")
                : "";

            return `
                <div class="quiz-item">

                    <h3>
                        ${index + 1}.
                        ${escapeHtml(item.question || "")}
                    </h3>

                    ${options}

                    <div class="answer">
                        <strong>Answer:</strong>
                        ${escapeHtml(item.answer || "")}
                    </div>

                    <div class="result-text">
                        ${escapeHtml(item.explanation || "")}
                    </div>

                </div>
            `;

        }).join("");

    } else {

        // Normal text result
        resultBox.innerHTML = `
            <div class="result-text">
                ${escapeHtml(data)}
            </div>
        `;
    }

    resultSection.classList.remove("hidden");
}


generateButton.addEventListener("click", async () => {

    const text = inputText.value.trim();

    if (!text) {

        statusBox.textContent =
            "Please enter a question, topic, or content.";

        return;
    }


    generateButton.disabled = true;

    statusBox.textContent =
        "Generating your result...";

    resultBox.innerHTML = "";

    resultSection.classList.add("hidden");


    try {

        const endpoint = endpoints[task.value];

        const response = await fetch(endpoint, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({

                task: task.value,

                text: text

            })

        });


        const data = await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail || "Request failed."
            );

        }


        renderResult(
            task.value,
            data.result
        );


        statusBox.textContent =
            "Done!";


    } catch (error) {

        console.error(error);

        statusBox.textContent =
            "Error: " + error.message;

    } finally {

        generateButton.disabled = false;

    }

});


clearButton.addEventListener("click", () => {

    inputText.value = "";

    resultBox.innerHTML = "";

    resultSection.classList.add("hidden");

    statusBox.textContent = "";

});