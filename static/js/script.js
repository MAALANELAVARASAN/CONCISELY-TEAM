// Wait for the DOM to be fully loaded before attaching the event listener
document.addEventListener('DOMContentLoaded', function() {
    // Get the form element by ID
    const form = document.getElementById('myForm');

    // Attach an onsubmit event to the form
    form.addEventListener('submit', function(event) {
        // Prevent the form from submitting normally
        event.preventDefault();

        // Redirect to another page
        window.location.href = "templates/about.html";
    });
});
