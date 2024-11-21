let isPaused = false;

// Function to toggle pause/resume state
function togglePause() {
    fetch('http://localhost:5001/pause_feed', {
        method: 'POST',
    })
    .then(response => response.json())
    .then(data => {
        isPaused = !isPaused;
        const btn = document.getElementById("pause-btn");
        // Update button text based on the paused state
        btn.textContent = isPaused ? "Resume Feed" : "Pause Feed";
    })
    .catch(error => console.error('Error:', error));
}