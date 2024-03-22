$(document).ready(function() {

    const searchParams = new URLSearchParams(window.location.search);

    $('#search-button').click(function(e) {
        var queryTerm = $('#search-bar').val();
        $('#search-query-parameter').attr("value", queryTerm);
        if($('#page-form').length) {
            $('#page-form').trigger("submit");
            e.preventDefault();
        }
    });
    $('#reset-button').click(function(e) {
        $('#search-bar').val("");
        if($('#page-form').length) {
            $('#page-form').trigger("submit");
        }
    });
    
    //Tooltips
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))
});

document.addEventListener("DOMContentLoaded", function() {
    // Get the profile dropdown menu element
    var profileDropdown = document.getElementById('profileDropdown');
    // Check if the user is authenticated
    var isAuthenticated = "{{ user.is_authenticated }}";

    if (isAuthenticated === "True") {
        // If user is authenticated, show the profile dropdown menu
        profileDropdown.style.display = 'block';
    } else {
        // If user is not authenticated, hide the profile dropdown menu
        profileDropdown.style.display = 'none';
    }
}); 

























































































