import { submitAnswer, endInterview } from "./api.js";

const sessionId = sessionStorage.getItem("session_id");
const question = sessionStorage.getItem("current_question");

document.getElementById("sessionId").innerText = `Session: ${sessionId}`;
document.getElementById("questionBox").innerText = question;

document.getElementById("submitBtn").addEventListener("click", async () => {
    const answer = document.getElementById("answerBox").value;
    if (!answer) return;

    const response = await submitAnswer(sessionId, answer);

    renderEvaluation(response.evaluation);

    if (response.state === "completed") {
        sessionStorage.setItem("report", JSON.stringify(response.report));
        window.location.href = "report.html";
    } else {
        sessionStorage.setItem("current_question", response.next_question);
        document.getElementById("questionBox").innerText = response.next_question;
        document.getElementById("answerBox").value = "";
    }
});

document.getElementById("endBtn").addEventListener("click", async () => {
    const response = await endInterview(sessionId);
    sessionStorage.setItem("report", JSON.stringify(response.report));
    window.location.href = "report.html";
});

function renderEvaluation(evaluation) {
    const panel = document.getElementById("evaluationPanel");

    panel.innerHTML = `
        <p>Technical Depth: ${evaluation.technical_depth}</p>
        <p>Accuracy: ${evaluation.accuracy}</p>
        <p>Clarity: ${evaluation.clarity}</p>
        <p>Confidence: ${evaluation.confidence}</p>
        <p><strong>Strengths:</strong> ${evaluation.strengths.join(", ")}</p>
        <p><strong>Weaknesses:</strong> ${evaluation.weaknesses.join(", ")}</p>
        <p><strong>Missing Concepts:</strong> ${evaluation.missing_concepts.join(", ")}</p>
    `;
}