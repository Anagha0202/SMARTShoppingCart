$(document).ready(function () {
    $.get('header.html', function(response) {
	    $('#header').html(response);
    });

    $('#btn-cart').click(function () {
    //this.increment("home");
            window.location.href = "/mycart";
            
            return false;
    });

    $('#btn-checkout').click(function () {
        window.location.href = "/checkout"
    })

    $('btn-logout').click(function () {
        window.location.href = "/logout";
    })

    /*$('#btn-del').click(function () {
	    var upc = $('#btn-del').val()
	    var upc_del = [{'upc_del': upc}]
	    $.ajax({
		    url = '/del',
		    data = JSON.stringify(upc_del),
		    contentType = "application/json", 
		    type = 'POST',
		    success: function(response) {
			    alert("Item deleted")
			   }
		    });
    });
	
   var source = new EventSource("{{ url_for('sse.stream') }}");
	source.addEventListener('publish', function(event) {
    	var data = JSON.parse(event.data);
    	alert(data);
	}, false);*/
});
