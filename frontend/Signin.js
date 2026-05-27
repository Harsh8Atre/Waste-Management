<<<<<<< HEAD
document.getElementById("signinForm").addEventListener("submit", function (e) {
    e.preventDefault();
    const email = document.getElementById("email").value;
    if (email) {
        localStorage.setItem("user", email);
        window.location.href = "index.html"; 
    }
});
=======
document.getElementById("signinForm").addEventListener("submit", function (e) {
    e.preventDefault();
    const email = document.getElementById("email").value;
    if (email) {
        localStorage.setItem("user", email);
        window.location.href = "index.html"; 
    }
});
>>>>>>> 8a91a168ef066bd31ac9c3bb5168b66d7c3a9006
