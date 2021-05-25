$(document).ready(function(){
	$("#dataframe").tablesorter();

	function monkey(){
		if (this.value.match(/[^\d\.]/g)){
			this.value = this.value.replace(/[^\d\.]/g,'');
		}
	}

document.querySelector('#flag').onkeyup = monkey;
});

$("#flag").on('change', function(){
	var val = parseFloat(this.value, 10);

	var id = $("th:contains('Рейтинг')").index()+1;

	$("table tr td:nth-child("+id+")").each(function(){

		if (parseFloat($(this).text())<val){

			$(this).css({'background':'#db3949'});

		}else if(parseFloat($(this).text())>val){

			$(this).css({'background':'#5bc78c'});
		}else{

			$(this).css({'background':'#faf75c'});
		}
	});
});