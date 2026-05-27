document.getElementById("signinForm").addEventListener("submit", function (e) {
    e.preventDefault();
    
    const emailElement = document.getElementById("email");
    if (emailElement) {
        const email = emailElement.value;
        if (email) {
            // Save user to localStorage for tracking across tabs
            localStorage.setItem("user", email);
            
            // Redirect smoothly back to the index template container context
            window.location.href = "index.html"; 
        }
    }
});