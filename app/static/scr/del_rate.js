function del(elem){
	$.ajax({ 
		type: 'POST',
		url: '/del_rate',
		success: function(data){
			window.location.replace('/account');
		},
		data: JSON.stringify(elem.id),
		dataType: 'json',
		headers: {
			'content-type':'application/json'
		}
	});
}