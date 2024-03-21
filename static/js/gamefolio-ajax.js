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
        }   
    })
})