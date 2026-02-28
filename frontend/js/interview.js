import { submitAnswer, endInterview } from "./api.js";

const sessionId = sessionStorage.getItem("session_id");
const question = sessionStorage.getItem("current_question");

if (!sessionId) {
    alert("No active session found. Please start interview again.");
    window.location.href = "index.html";
}

document.getElementById("sessionId").innerText = `Session: ${sessionId}`;

let questionCount = 0;
let performanceData = [];

// ==============================
// CHAT MESSAGE HANDLER
// ==============================

function addMessage(content, type) {
    const container = document.getElementById("chatContainer");

    const msg = document.createElement("div");
    msg.classList.add("message");

    if (type === "ai") {
        msg.classList.add("ai-message");
    } else {
        msg.classList.add("user-message");
    }

    msg.innerText = content;

    container.appendChild(msg);
    container.scrollTop = container.scrollHeight;
}

// Show first AI message
if (question) {
    addMessage(question, "ai");
}

// ==============================
// SUBMIT ANSWER
// ==============================

document.getElementById("submitBtn").addEventListener("click", async () => {

    const answerBox = document.getElementById("answerBox");
    const answer = answerBox.value.trim();

    if (!answer) return;

    addMessage(answer, "user");
    answerBox.value = "";

    try {
        const response = await submitAnswer(sessionId, answer);

        if (!response || !response.evaluation) {
            console.error("Backend error:", response);
            alert("Session expired or invalid. Restart interview.");
            sessionStorage.clear();
            window.location.href = "index.html";
            return;
        }

        // Add next AI message
        addMessage(response.next_question, "ai");

        // Store next question
        sessionStorage.setItem("current_question", response.next_question);

        // Save performance
        questionCount++;
        performanceData.push(response.evaluation.technical_depth);

        renderEvaluation(response.evaluation);

        // Show analytics after 5 questions
        if (questionCount >= 5) {
            showAnalytics();
        }

        if (response.state === "completed") {
            sessionStorage.setItem("report", JSON.stringify(response.report));
            sessionStorage.clear();
            window.location.href = "report.html";
        }

    } catch (err) {
        console.error(err);
        alert("Request failed. Restart interview.");
        sessionStorage.clear();
        window.location.href = "index.html";
    }
});

// ==============================
// END INTERVIEW
// ==============================

document.getElementById("endBtn").addEventListener("click", async () => {

    try {
        const response = await endInterview(sessionId);

        if (!response.report) {
            alert("Session expired.");
            sessionStorage.clear();
            window.location.href = "index.html";
            return;
        }

        sessionStorage.setItem("report", JSON.stringify(response.report));
        sessionStorage.clear();
        window.location.href = "report.html";

    } catch (err) {
        console.error(err);
        alert("Session expired.");
        sessionStorage.clear();
        window.location.href = "index.html";
    }
});

// ==============================
// EVALUATION SUMMARY PANEL
// ==============================

function renderEvaluation(evaluation) {
    const panel = document.getElementById("evaluationSummary");

    panel.innerHTML = `
        <p><b>Technical Depth:</b> ${evaluation.technical_depth}</p>
        <p><b>Accuracy:</b> ${evaluation.accuracy}</p>
        <p><b>Clarity:</b> ${evaluation.clarity}</p>
        <p><b>Confidence:</b> ${evaluation.confidence}</p>
        <p><b>Strengths:</b> ${evaluation.strengths.join(", ")}</p>
        <p><b>Weaknesses:</b> ${evaluation.weaknesses.join(", ")}</p>
    `;
}

// ==============================
// GRAPH SECTION
// ==============================

function showAnalytics() {

    const section = document.getElementById("analyticsSection");
    section.style.display = "block";

    const ctx = document.getElementById("performanceChart").getContext("2d");

    new Chart(ctx, {
        type: "line",
        data: {
            labels: performanceData.map((_, i) => `Q${i + 1}`),
            datasets: [{
                label: "Technical Depth",
                data: performanceData,
                borderColor: "#2563eb",
                backgroundColor: "rgba(37,99,235,0.2)",
                fill: true,
                tension: 0.3
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 10
                }
            }
        }
    });
}