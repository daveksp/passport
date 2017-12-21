$(document).ready(function(){
	
	var url = ''
	var type = '';
    if(location.pathname.startsWith('/passport/admin/clients')){
		url = '/passport/api/v1/auth/clients';
		type = 'clients';
	} else{
		url = '/passport/api/v1/auth/roles';
		type = 'roles';
	}


	$('.tags').tagsinput({
	  typeaheadjs: {
	    name: 'urls',
	    displayKey: 'name',
	    valueKey: 'name',
	    source: []
	  }
	});


	$(":submit").on('click', function(){
		var data = {};
		
		var id = $("input[name=id]").val();
		var method = 'POST'; 

		if(type=='clients'){
			data.name = $("input[name=name]").val();
			data.description = $("input[name=description]").val();
			data.redirect_uris = $("input[name=redirect_uris]").val();
		} else{
			data.name = $("input[name=name]").val();
			data.description = $("input[name=description]").val();
		}

		if(id != 0){
			method = 'PUT';
			url += '/' + id;
			data.id = id;
		}
		
		$('.result').empty();
		$.ajax({
			method: method,
			url: url,
			data: JSON.stringify(data),
			contentType: "application/json; charset=utf-8"
		}).done(function(msg){
			$('.result').append('<p class="bg-success">Success</p>')
			console.log('success');
		}).fail(function(jqXHR, textStatus){
			$('.result').append('<p class="bg-danger">An error occurred.</p>')
			console.log('something went terribly wrong :(');
		});
	})
})