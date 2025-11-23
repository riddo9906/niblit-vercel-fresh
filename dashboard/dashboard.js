// Simple dashboard UI logic
function updateDashboard(data) {
    const panel = document.getElementById("dashboard-panel");
    panel.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
}
