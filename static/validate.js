function validateEntry(){
    var x = document.getElementById("uname").value;
    var y = document.getElementById("validatepass").value;
    var z= document.getElementById("validateEmail").value;
    var a= document.getElementById("fname").value;
    var b= document.getElementById("lname").value;
    var c= document.getElementById("validateConfirmation").value;
    var letters = /^[A-Za-z]+$/;
    var emailconfirm = /^[^\s@]+@[^\s@]+$/;
    if (x==""){
        alert("Please enter a username");
    }
    else if(y==""){
        alert("Please enter a password");
    }
    else if(z==""){
        alert("Please enter an email");
    }
    else if(a==""){
        alert("Please enter a first name");
    }
    else if(b==""){
        alert("Please enter a last name");
    }
    else if(c==""){
        alert("Confirm password is empty");
    }
    else if(y!=c)
    {
        alert("Passwords do not match");
    }

    else if(!letters.test(a))
    {
        alert("First name has numbers");
    }
    else if(!letters.test(b))
    {
        alert("Last name has numbers");
    }
    else if(!emailconfirm.test(z))
    {
        alert("Invaild Email address");
    }

}
