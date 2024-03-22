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
    
    const reviewsPerPage = 4;
    var currentPage = 1;
    var currentReviews= Array.from(Array(reviewsPerPage).keys())
    var maxPage = Math.floor($(".user-review").toArray().length/reviewsPerPage)+1;
    console.log(maxPage);
    paginateReviews();

    function paginateReviews() {
        const userReviews = $(".user-review").each(function(i, el) {
            if(!currentReviews.includes(i)) {
                $(this).addClass("d-none");
            } else {
                $(this).removeClass("d-none");
            }
        })
        $("#current-review-page").text(currentPage);
        $("#prev-review-button").removeClass("disabled");
        $("#next-review-button").removeClass("disabled");
        
        if(currentPage == 1) {
            $("#prev-review-button").addClass("disabled");
        }
        if(currentPage == maxPage) {
            $("#next-review-button").addClass("disabled");
        }
    }

    $("#next-review-button").click(function() {
        currentPage++
        for (let i = 0; i < currentReviews.length; i++) {
            currentReviews[i] += 8;
        }
        paginateReviews();
    })

    $("#prev-review-button").click(function() {
        currentPage--;
        for (let i = 0; i < currentReviews.length; i++) {
            currentReviews[i] -= 8;
        }
        paginateReviews();
    })

    //Tooltips
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))
});