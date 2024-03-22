$(document).ready(function() {
    
    $("#search-bar").autocomplete({
        source: function(request, response) {
            var query;
            query = $("#search-bar").val();
            $.ajax({
                url: '/gamefolio_app/suggest/?suggestion='+query,
                success: function(data) {
                    response(data.split(","))
                }
            });
        },
        select: function(event, ui) {
            $('#search-query-parameter').attr("value", ui.item.value);
            $("#search-form").submit();
        }
    })
})

$(document).ready(function() {
    $('.like_btn').click(function() {
        var reviewIdVar;
        reviewIdVar = $(this).attr('data-reviewid');

        $.get('/gamefolio/like_review/',
            {'review_id': reviewIdVar},
            function(data) {
                console.log(data)
                $(this).siblings("#like_count").html(data);
                $(this).hide();
            }
        );
    });
});

