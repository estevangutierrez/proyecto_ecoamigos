const loginBtn = document.getElementById('loginButton');

loginBtn.addEventListener('click',()=> {
    const usuario = document.getElementById('username').value;
    const contrasena = document.getElementById('password').value;

    const formData = {
        usuario: usuario,
        contrasena: contrasena
    };

    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json' 
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        if(data.success){
            window.location.href = data.redirect_url;
        } else {
            Swal.fire("¡Ups!","Los datos ingresados no son válidos","error")
        }
    })
    .catch(error => {
        console.error('Error: ' + error)
    })
});