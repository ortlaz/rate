$(function(){
	$(".items-list").selectable();
});

$('#add-from-list').on('click', function(){
	var i = 1;

	if ($("li").is(".par")){
		i = parseInt($("li.par").filter(":last").attr("id"),10)+1;
	}

	$('li.ui-selected').each(function(){

		var data = $(this).text().replace(/[\t\n]+/g,'');
		var flag = false;

		if (i>1){
			$("li.par").each(function(){if ($(this).text() == data){flag=true;}});
		}

		if (flag == true) {
			$("div.error-container").html("Error");
		}else{
			$("div.error-container").html("");
			$("ul.parameters").append('<li class="par" id="'+i+'"></li>');
			$("#"+i+".par").html(data+'<button onclick="del(this)" class = "del" id="'+i+'"></button>');
			i += 1;
		}
	});
});

var paramsObj = [];

function addParameter(array){
	var formula = $("#parameter").val();
	var name = $("#param-name").val();
	var dict = {};

	var flag = false;
	
	var i = 1;
	
	if ($("li").is(".par")){
		i = parseInt($("li.par").filter(":last").attr("id"),10)+1;
	}

	if (i>1){
		$("li.par").each(function(){if ($(this).text() == name){flag=true;}});
	}

	if (flag == true) {
		$("div.error-field").html("Error");
	}else{

		dict["name"] = name;
		dict["formula"] = formula;
		array.push(dict);

		$("div.error-field").html("");
		$("ul.parameters").append('<li class="par" id="'+i+'"></li>');
		$("#"+i+".par").html(name+'<button onclick="del(this)" class = "del" id="'+i+'">');
	}

}

$("#add-from-user").on('click', function(){
	// var paramsObj = [];
	addParameter(paramsObj);

});

function setArray(array){ 
	var list = [];

	$('li.par').each(function(){
		list.push($(this).text().replace(/[\t\n]+/g,''));
	});

	list.forEach(function(item, i ,arr){
		var flag = false;
		array.forEach(function(el,j,mas){

			if (el['name'] == item){
				flag = true;
			}
		});
		
		if (flag!=true){
			array.push({"name":item, "formula":''});
		}		
	});
}

$("#continue").on('click', function(){
	// var paramsObj = [];
	setArray(paramsObj);
	$.ajax({ 
		type: 'POST',
		url: '/chooseparams',
		success: function(data){
			window.location.replace('/finish');
		},
		data: JSON.stringify(paramsObj),
		dataType: 'json',
		headers: {
			'content-type':'application/json'
		}
	});
	
});

function del(elem){

	console.log(elem);
		paramsObj.forEach(function(el,j,mas){

			if 	($("#"+elem.id+".par").text().replace(/[\t\n]+/g,'')==el['name']){
				mas.splice(mas.indexOf(el),1);
			}
		});
		$("li#"+elem.id+".par").remove();
}



