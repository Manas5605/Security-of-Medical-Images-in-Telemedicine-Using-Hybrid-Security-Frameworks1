document.getElementById("stegoForm").addEventListener("submit", function(event) {
    event.preventDefault();

    let formData = new FormData();
    let stegoImage = document.getElementById("stegoInput").files[0];

    if (!stegoImage) {
        alert("Please select an image.");
        return;
    }

    formData.append("image", stegoImage);

    fetch("/steganography/apply_stego", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Display Stego Image and Histogram
            document.getElementById("stegoImage").src = data.stego_image + "?" + new Date().getTime();
            document.getElementById("stegoHistogram").src = data.stego_histogram + "?" + new Date().getTime();
            document.getElementById("stegoResults").classList.remove("hidden");

            // Show the "Proceed to Encryption" button
            document.getElementById("nextButton").classList.remove("hidden");
        } else {
            alert("Error: " + data.error);
        }
    })
    .catch(error => console.error("Error:", error));
});

// Handle Next Button Click - Proceed to Encryption Page
document.getElementById("nextButton").addEventListener("click", function() {
    window.location.href = "/encryption";  // Ensure this is the correct path to your encryption page
});
