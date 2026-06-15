document.getElementById("showSignup").addEventListener("click", function() {
    document.getElementById("loginForm").style.display = "none";
    document.getElementById("signupForm").style.display = "block";
});

document.getElementById("showLogin").addEventListener("click", function() {
    document.getElementById("signupForm").style.display = "none";
    document.getElementById("loginForm").style.display = "block";
});

// Handle login form submission
document.getElementById("loginFormContent").addEventListener("submit", async function(event) {
    event.preventDefault();
    
    let username = document.getElementById("username").value;
    let password = document.getElementById("password").value;

    let response = await fetch("/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
    });

    let data = await response.json();

    if (data.success) {
        window.location.href = "/admin-dashboard"; // Redirect to admin dashboard
    } else {
        alert(data.message);
    }
});

// Handle signup form submission
document.getElementById("signupFormContent").addEventListener("submit", async function(event) {
    event.preventDefault();

    let newUsername = document.getElementById("newUsername").value;
    let newPassword = document.getElementById("newPassword").value;
    let confirmPassword = document.getElementById("confirmPassword").value;

    if (newPassword !== confirmPassword) {
        alert("Passwords do not match.");
        return;
    }

    let response = await fetch("/signup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: newUsername, password: newPassword })
    });

    let data = await response.json();

    if (data.success) {
        alert("Signup successful. You can now log in.");
        document.getElementById("signupForm").style.display = "none";
        document.getElementById("loginForm").style.display = "block";
    } else {
        alert(data.message);
    }
});
