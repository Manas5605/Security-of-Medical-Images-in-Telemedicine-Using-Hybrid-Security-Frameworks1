document.getElementById("uploadForm").addEventListener("submit", function(event) {
    event.preventDefault();

    let formData = new FormData();
    let imageInput = document.getElementById("imageInput").files[0];

    if (!imageInput) {
        alert("Please select an image.");
        return;
    }

    formData.append("image", imageInput);

    fetch("/watermarking/apply_watermark", {  // Corrected URL
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Update the images
            document.getElementById("watermarkedImage").src = data.watermarked_image + "?" + new Date().getTime();
            document.getElementById("histogramImage").src = data.histogram + "?" + new Date().getTime();

            // Show the result section
            document.getElementById("result").classList.remove("hidden");
        } else {
            alert("Error: " + data.error);
        }
    })
    .catch(error => console.error("Error:", error));
});
