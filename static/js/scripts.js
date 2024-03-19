$(document).ready(function() {

    const searchParams = new URLSearchParams(window.location.search);
    var ratingConfirmed = false;
    
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

    //Ratings
    function calculateSize(e) {
        var rating = calculateRating(e);
        var width = $("#rating-input").width();
        const halfStarSize = width/10;
        var newWidth = width * (rating/10);
        var newWidth = newWidth - (newWidth % halfStarSize)

        return newWidth;
    }

    function calculateRating(e) {
        var mouseX = e.pageX;
        var left = $("#rating-hover").position().left;
        var width = $("#rating-input").width();
        var relativeMouseX = mouseX-left;
        var percentage = relativeMouseX/width + 0.095;
        if(percentage < 0.1) {
            percentage = 0.1;
        }
        return Math.floor(10*percentage);
    }

    $('#rating-input').mousemove(function(e) {
        $("#rating-actual").addClass("d-none");
        $("#rating-hover").get(0).style.setProperty("--width", calculateSize(e)+"px");
    });
    
    $('#rating-input').mouseleave(function(e) {
        $("#rating-actual").removeClass("d-none");
        $("#rating-hover").get(0).style.setProperty("--width", "0px");
    });

    $('#rating-input').click(function(e) {
        $("#rating-actual").removeClass("d-none");
        $("#rating-value").attr("value", calculateRating(e));
        $("#rating-actual").get(0).style.setProperty("--width", calculateSize(e) + "px");
        $("#rating-hover").get(0).style.setProperty("--width", "0px");
    });

    //Tooltips
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))
});

