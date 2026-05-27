let maxPredictions;

// Predict image by sending it to your unified backend API endpoint
async function predictImage(imageElement) {
    try {
        const canvas = document.createElement('canvas');
        canvas.width = imageElement.width || imageElement.naturalWidth;
        canvas.height = imageElement.height || imageElement.naturalHeight;
        
        const ctx = canvas.getContext('2d');
        ctx.drawImage(imageElement, 0, 0);
        
        const blob = await new Promise(resolve => canvas.toBlob(resolve, 'image/jpeg'));
        const formData = new FormData();
        formData.append('file', blob, 'image.jpg');

        // Dynamically detects if running locally or on Streamlit Cloud
        const backendHost = window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1" 
            ? "http://127.0.0.1:8000" 
            : window.location.origin;

        const response = await fetch(`${backendHost}/predict/`, {    
            method: "POST",
            body: formData
        });

        if (!response.ok) throw new Error("API request failed");

        const result = await response.json();
        if (result.predictions && result.predictions.length > 0) {
            const top = result.predictions[0];
            document.getElementById("result").innerText =
                `Predicted Waste Category: ${top.class} (${(top.confidence * 100).toFixed(2)}%)`;
        } else {
            document.getElementById("result").innerText = "No objects detected.";
        }
    } catch (error) {
        console.error("Prediction Error:", error);
        document.getElementById("result").innerText = "Error matching categories from API server.";
    }
}

// Handle uploaded image
document.getElementById("imageUpload").addEventListener("change", async function (event) {
    const file = event.target.files[0];
    if (!file) return;

    const imgElement = document.getElementById("uploadedImage");
    imgElement.src = URL.createObjectURL(file);
    imgElement.style.display = "block";

    imgElement.onload = async () => {
        await predictImage(imgElement);
    };
});

// Show webcam when button clicked
document.getElementById("showWebcam").addEventListener("click", () => {
    const webcamSection = document.getElementById("webcamSection");
    if (webcamSection) webcamSection.style.display = "block";

    // Start webcam stream
    navigator.mediaDevices.getUserMedia({ video: true })
        .then((stream) => {
            const videoEl = document.getElementById("video");
            if (videoEl) videoEl.srcObject = stream;
        })
        .catch((err) => {
            console.error("Error accessing webcam:", err);
        });
});

// Handle webcam capture
document.getElementById("capture").addEventListener("click", async () => {
    const video = document.getElementById("video");
    const canvas = document.getElementById("canvas");
    
    if (!video || !canvas) return;
    
    const context = canvas.getContext("2d");
    const uploadedImage = document.getElementById("uploadedImage");

    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    const dataURL = canvas.toDataURL("image/png");

    if (uploadedImage) {
        uploadedImage.src = dataURL;
        uploadedImage.style.display = "block";
    }

    const img = new Image();
    img.src = dataURL;
    img.onload = async () => {
        await predictImage(img);
    };

    if (!localStorage.getItem("user")) {
        window.location.href = "signin.html";
    }
});

// On window load
window.onload = function () {
    // User greeting
    const user = localStorage.getItem("user");
    const logoEl = document.getElementById("logo");
    if (user && logoEl) {
        logoEl.innerText = "Welcome To SmartSort Solutions";
    }
};