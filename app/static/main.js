function change(elem){
	$.ajax({ 
		type: 'POST',
		url: '/edit',
		data: JSON.stringify(elem.id),
		dataType: 'json',
		headers: {
			'content-type':'application/json'
		}
	});

	window.location.replace('/edit');
}

function build(elem){
	$.ajax({ 
		type: 'POST',
		url: '/build',
		data: JSON.stringify(elem.id),
		dataType: 'json',
		headers: {
			'content-type':'application/json'
		}
	});
	window.location.replace('/build');
}