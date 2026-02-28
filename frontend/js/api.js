const BASE_URL = "http://127.0.0.1:8000";

async function request(endpoint, method = "GET", body = null) {
    const options = {
        method,
        headers: { "Content-Type": "application/json" }
    };

    if (body) {
        options.body = JSON.stringify(body);
    }

    const response = await fetch(`${BASE_URL}${endpoint}`, options);

    if (!response.ok) {
        const err = await response.json();
        throw new Error(err.detail || "Server error");
    }

    return response.json();
}

export async function startInterview(resume, jobDescription) {
    return request("/start", "POST", {
        resume,
        job_description: jobDescription
    });
}

export async function submitAnswer(sessionId, answer) {
    return request("/answer", "POST", {
        session_id: sessionId,
        answer
    });
}

export async function endInterview(sessionId) {
    return request("/end", "POST", {
        session_id: sessionId
    });
}