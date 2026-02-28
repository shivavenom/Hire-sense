const report = JSON.parse(sessionStorage.getItem("report"));

const container = document.getElementById("reportContent");

container.innerHTML = `
    <h2>Overall Score: ${report.overall_score}</h2>
    <p>${report.technical_summary}</p>
    <p>${report.communication_summary}</p>
    <h3>Strengths</h3>
    <ul>${report.strengths.map(s => `<li>${s}</li>`).join("")}</ul>
    <h3>Areas for Improvement</h3>
    <ul>${report.areas_for_improvement.map(a => `<li>${a}</li>`).join("")}</ul>
    <h3>Recommendations</h3>
    <ul>${report.recommendations.map(r => `<li>${r}</li>`).join("")}</ul>
`;