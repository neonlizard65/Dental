
//При выборе врача из списка врачей, отправляется get запрос по id врача. Мы получаем по ссылке json, который содержит все свободные времена для приема
doctor.onchange = () => {
    document.getElementById("time").innerHTML = "";
    document.getElementById("time").style.visibility = 'visible';
    doctorid = doctor.value;
    fetch("http://127.0.0.1:8000/get/schedule?doctor="+doctorid).then((response) =>{
        
        response.json().then((data) =>{
            optionHTML = '<option disabled selected value> -- Выберите время -- </option>';
            for(time of data.schedule){
                optionHTML += '<option value="' + time.id + '">' + time.day_of_week + ' - ' + time.start_time + '</option>';
            }
            document.getElementById("time").innerHTML = optionHTML;
        });
    });
}; 