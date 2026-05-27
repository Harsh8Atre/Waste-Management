window.onload = function () {
    const user = localStorage.getItem("user");

    if (user) {
        // Safe check to ensure 'logo' element exists before mutating text
        const logoEl = document.getElementById("logo");
        if (logoEl) {
            logoEl.innerText = "Welcome, " + user;
        }

        incrementActiveTruckCount();
        updateActiveTruckEmails(user);
    }
};

function incrementActiveTruckCount() {
    let activeTruckCount = parseInt(localStorage.getItem("activeTruckCount") || "0");
    
    activeTruckCount++;
    localStorage.setItem("activeTruckCount", activeTruckCount);

    const countEl = document.getElementById("activeTruckCount");
    if (countEl) {
        countEl.textContent = activeTruckCount;
    }

    console.log("Active truck count: " + activeTruckCount);
}

function updateActiveTruckEmails(user) {
    let activeTruckEmails = JSON.parse(localStorage.getItem("activeTruckEmails") || "[]");

    const truckEmail = user + "@truck.com"; 
    activeTruckEmails.push(truckEmail);

    localStorage.setItem("activeTruckEmails", JSON.stringify(activeTruckEmails));

    const emailList = document.getElementById("activeTruckEmails");
    if (emailList) {
        emailList.innerHTML = "";
        activeTruckEmails.forEach(email => {
            const listItem = document.createElement("li");
            listItem.textContent = email;
            emailList.appendChild(listItem);
        });
    }

    console.log("Active truck emails: ", activeTruckEmails);
}