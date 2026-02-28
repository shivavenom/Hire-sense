import { CONFIG } from "../config.js";

export async function startInterview(resume, jobDescription) {
    const response = await fetch(`${CONFIG.BASE_URL}/start`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            resume: resume,
            job_description: jobDescription
        })
    });

    return await response.json();
}

export async function submitAnswer(sessionId, answer) {
    const response = await fetch(`${CONFIG.BASE_URL}/answer`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            session_id: sessionId,
            answer: answer
        })
    });

    return await response.json();
}

export async function endInterview(sessionId) {
    const response = await fetch(`${CONFIG.BASE_URL}/end`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            session_id: sessionId
        })
    });

    return await response.json();
}