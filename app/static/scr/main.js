function change(elem){

	$.ajax({ 
		type: 'POST',
		url: '/edit',
		success: function(data){
			window.location.replace('/upload');
		},
		data: JSON.stringify(elem.id),
		dataType: 'json',
		headers: {
			'content-type':'application/json'
		}
	});

	// window.location.replace('/edit');
}

function build(elem){
	$.ajax({ 
		type: 'POST',
		url: '/build',
		success: function(data){
			window.location.replace('/upload');
		},
		data: JSON.stringify(elem.id),
		dataType: 'json',
		headers: {
			'content-type':'application/json'
		}
	});

	// window.location.replace('/build');
}

function create(){
	window.location.replace('/upload')
}