document.getElementById("signinForm").addEventListener("submit", function (e) {
    e.preventDefault();
    const email = document.getElementById("email").value;
    if (email) {
        localStorage.setItem("user", email);
        window.location.href = "index.html"; 
    }
});
