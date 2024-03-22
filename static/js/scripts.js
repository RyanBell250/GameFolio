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
    var currentReviewPage = 1;
    var currentReviews= Array.from(Array(reviewsPerPage).keys())
    var maxReviewPage = Math.ceil($(".user-review").toArray().length/reviewsPerPage)+1;
    console.log(maxReviewPage);
    paginateReviews();

    function paginateReviews() {
        const userReviews = $(".user-review").each(function(i, el) {
            if(!currentReviews.includes(i)) {
                $(this).addClass("d-none");
            } else {
                $(this).removeClass("d-none");
            }
        })
        $("#current-review-page").text(currentReviewPage);
        $("#prev-review-button").removeClass("disabled");
        $("#next-review-button").removeClass("disabled");
        
        if(currentReviewPage == 1) {
            $("#prev-review-button").addClass("disabled");
        }
        if(currentReviewPage >= maxReviewPage) {
            $("#next-review-button").addClass("disabled");
        }
        if(maxReviewPage <= 1) {
            $("#prev-list-button").addClass("d-none");
            $("#next-list-button").addClass("d-none");
            $("#current-list-page").addClass("d-none");

        }
    }

    $("#next-review-button").click(function() {
        currentReviewPage++
        for (let i = 0; i < currentReviews.length; i++) {
            currentReviews[i] += reviewsPerPage;
        }
        paginateReviews();
    })

    $("#prev-review-button").click(function() {
        currentReviewPage--;
        for (let i = 0; i < currentReviews.length; i++) {
            currentReviews[i] -= reviewsPerPage;
        }
        paginateReviews();
    })

    const listsPerPage = 6;
    var currentListPage = 1;
    var currentLists = Array.from(Array(listsPerPage).keys())
    var maxListPage = Math.ceil($(".user-list").toArray().length/listsPerPage);
    paginateLists();

    function paginateLists() {
        const userLists = $(".user-list").each(function(i, el) {
            if(!currentLists.includes(i)) {
                $(this).addClass("d-none");
            } else {
                $(this).removeClass("d-none");
            }
        })
        $("#current-list-page").text(currentListPage);
        $("#prev-list-button").removeClass("disabled");
        $("#next-list-button").removeClass("disabled");
        
        if(currentListPage == 1) {
            $("#prev-list-button").addClass("disabled");
        }
        if(currentListPage >= maxListPage) {
            $("#next-list-button").addClass("disabled");
        }

        if(maxListPage <= 1) {
            $("#prev-list-button").addClass("d-none");
            $("#next-list-button").addClass("d-none");
            $("#current-list-page").addClass("d-none");

        }
    }

    $("#next-list-button").click(function() {
        currentListPage++
        for (let i = 0; i < currentLists.length; i++) {
            currentLists[i] += listsPerPage;
        }
        paginateLists();
    })

    $("#prev-list-button").click(function() {
        currentListPage--;
        for (let i = 0; i < currentLists.length; i++) {
            currentLists[i] -= listsPerPage;
        }
        paginateLists();
    })

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

