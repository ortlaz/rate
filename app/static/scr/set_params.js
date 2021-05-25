$(document).ready(function(){
	$('#build').attr('disabled',true);
	$('#save').attr('disabled',true);

	var id = parseInt($("input.weight").filter(":last").attr("id"),10)+1;

	for (var i =0;i<id;i++){
		$('input[id_min='+i+']').prop('checked',false);
		$('input[id_max='+i+']').prop('checked',false);

	}


});

function monkey(){
		if (this.value.match(/[^\d\.]/g)){
			this.value = this.value.replace(/[^\d\.]/g,'');
		}
	}

document.querySelectorAll('.weight').forEach(function(item){
	item.onkeyup = monkey;
}); 

function check_box(elem){

	var cls = $(elem).attr('class');

		if (cls == 'max'){
			var num = $(elem).attr('id_max');
			if (elem.checked){
				$('input[id_min='+num+']').attr('disabled', true);
			}else{
				$('input[id_min='+num+']').removeAttr('disabled');	
			}

		}else if (cls == 'min'){
			var num = $(elem).attr('id_min');
			if (elem.checked){	
				$('input[id_max='+num+']').attr('disabled', true);
			}else{
				$('input[id_max='+num+']').removeAttr('disabled');	
			}
	}

}

function btn_activate(){

	var weights = {};
	var maxmin = {};

	var id = parseInt($("input.weight").filter(":last").attr("id"),10)+1;

	for (var i =0;i<id;i++){
		if ($('input[id_max='+i+']').attr('disabled')){
			maxmin[$("td#"+i+".pars.names").text().replace(/[\t\n]+/g,'')]= [0,1];

		} else if ($('input[id_min='+i+']').attr('disabled')){
			maxmin[$("td#"+i+".pars.names").text().replace(/[\t\n]+/g,'')]= [1,0];
		}else{
			maxmin[$("td#"+i+".pars.names").text().replace(/[\t\n]+/g,'')]= [0,0];
		}

	}

	if ($("input#name").val() != ''){
		weights['rate_name'] = $("input#name").val();
		weights['rate_formula'] = $("div#rate-form").text().replace(/[\t\n]+/g,'');
		weights['data'] = weight_list;
		weights['flags'] = maxmin;

	}else{
		$('div.form-errors').append('<p>Введите название для рейтинга.</p>');

	}

	if ($('#build').attr('disabled') && Object.keys(weights).length){
		$('#build').removeAttr('disabled');
	}

	$.ajax({ 
		type: 'POST',
		url: '/finish',
		data: JSON.stringify(weights),
		dataType: 'json',
		headers: {
			'content-type':'application/json'
		}
	});

}

var weight_list = {};

function create_formula(){

	var sum = 0;

	var id = parseInt($("input.weight").filter(":last").attr("id"),10)+1;

	for (var i =0;i<id;i++){

		if (($("input#"+i+".weight")) && (parseFloat($("input#"+i+".weight").val())>=0)){

			if (parseFloat($("input#"+i+".weight").val())<1){

				sum += parseFloat($("input#"+i+".weight").val());
				weight_list[$("td#"+i+".pars.names").text().replace(/[\t\n]+/g,'')]= $("input#"+i+".weight").val();

			}else{
				$('div.tbl-errors').append('<p>Значение каждого веса должно быть меньше 1 и больше 0.</p>');
			}

		}
	}

	if (sum != 1){
		$('div.tbl-errors').append('<p>Сумма значений весов должна равняться 1.</p>');
	}else{
		if ($('#save').attr('disabled')){
			$('#save').removeAttr('disabled');
		}
	}

	var formula = '';

	for ([key, value] of Object.entries(weight_list) ){
		if (formula){
			formula += '+';
		}
		formula += key+ '*'+value;
	}

	formula = 1000+'*'+'('+formula+')';
	$('div#rate-form').html(formula);

}