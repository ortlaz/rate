let label = document.getElementById('download-file').nextElementSibling, 
    labelVal = label.querySelector('.download-text').innerText;

  
document.getElementById('download-file').addEventListener('change', function (e) {

  filename = document.getElementById('download-file').files[0].name;
  if (filename){
     label.querySelector('.download-text').innerText = 'Выбран файл: ' + filename;    
  }
  else
      label.querySelector('.download-text').innerText = labelVal;
});
