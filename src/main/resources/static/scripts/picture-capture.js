let videoStream;

async function startCamera() {
    try {
        videoStream = await navigator.mediaDevices.getUserMedia({ video: true });
        const videoElement = document.getElementById("camera");
        videoElement.srcObject = videoStream;
        videoElement.play();
    } catch (error) {
        console.error("Error accessing camera: ", error);
        alert("Unable to access the camera. Please allow camera permissions.");
    }
}

function capturePhoto() {
    const videoElement = document.getElementById("camera");
    const canvas = document.getElementById("photoCanvas");
    const context = canvas.getContext("2d");
    context.drawImage(videoElement, 0, 0, canvas.width, canvas.height);

    const imageDataUrl = canvas.toDataURL("image/png");
    document.getElementById("photoData").value = imageDataUrl;

    alert("Photo captured successfully!");
}

function stopCamera() {
    if (videoStream) {
        const tracks = videoStream.getTracks();
        tracks.forEach(track => track.stop());
    }
}

window.addEventListener("beforeunload", stopCamera);