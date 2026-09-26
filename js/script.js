document.addEventListener("DOMContentLoaded", function () {

    console.log("Smart Study Planner loaded successfully.");

    const dateInputs = document.querySelectorAll(
        'input[type="date"]'
    );

    const today = new Date()
        .toISOString()
        .split("T")[0];

    dateInputs.forEach(function (input) {
        input.setAttribute("min", today);
    });

});
