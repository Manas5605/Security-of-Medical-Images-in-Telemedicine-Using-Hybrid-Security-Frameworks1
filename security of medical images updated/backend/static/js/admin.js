document.getElementById("logoutBtn").addEventListener("click", function() {
    // Redirect to the login page on logout
    window.location.href = "/";
});

document.getElementById("uploadBtn").addEventListener("click", function() {
    // Redirect to the watermarking page when the "Upload Image" button is clicked
    window.location.href = "/watermarking"; // Make sure the route for watermarking is correct
});
