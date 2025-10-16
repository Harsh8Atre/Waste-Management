window.onload = function () {
    const user = localStorage.getItem("user");

    if (user) {
        document.getElementById("logo").innerText = "Welcome, " + user;

        incrementActiveTruckCount();

        updateActiveTruckEmails(user);
    }
};

function incrementActiveTruckCount() {
    let activeTruckCount = parseInt(localStorage.getItem("activeTruckCount") || "0");
    
    activeTruckCount++;

    localStorage.setItem("activeTruckCount", activeTruckCount);

    document.getElementById("activeTruckCount").textContent = activeTruckCount;

    console.log("Active truck count: " + activeTruckCount);
}

function updateActiveTruckEmails(user) {
    let activeTruckEmails = JSON.parse(localStorage.getItem("activeTruckEmails") || "[]");

    const truckEmail = user + "@truck.com"; 
    activeTruckEmails.push(truckEmail);

    localStorage.setItem("activeTruckEmails", JSON.stringify(activeTruckEmails));

    const emailList = document.getElementById("activeTruckEmails");
    emailList.innerHTML = "";
    activeTruckEmails.forEach(email => {
        const listItem = document.createElement("li");
        listItem.textContent = email;
        emailList.appendChild(listItem);
    });

    console.log("Active truck emails: ", activeTruckEmails);
}
