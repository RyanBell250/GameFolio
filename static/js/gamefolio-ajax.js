
$('#search-bar').keyup(function() { 
    var query;
    query = $(this).val();

        $.get('/gamefolio_app/suggest/',
              {'suggestion': query},
              function(data) { 
                $('#search-results').html(data);
            }) 
});