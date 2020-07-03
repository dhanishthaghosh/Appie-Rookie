function validate(){
    if (document.getElementById('fname').value == '') {
        alert('Please enter first name!');
    }

    if (document.getElementById('lname').value == '') {
        alert('Please enter last name!');
    }

    if (document.getElementById('id_num').value == '') {
        alert('Please enter id_num!');
    }
    
    if (document.getElementById('email').value == '') {
        alert('Please enter email id!');
    }
}

function nextPage(){
    window.location= "../html/signup_2.html";
}