document.addEventListener('DOMContentLoaded', function () {
    const loginBtn = document.getElementById('loginButton');
    const pass = document.getElementById('password');
    const user = document.getElementById('username');
    const loadingOverlay = document.getElementById('loadingOverlay');

    function showLoadingOverlay() {
        loadingOverlay.style.display = 'block';
    }

    function hideLoadingOverlay() {
        loadingOverlay.style.display = 'none';
    }

    function login() {
        showLoadingOverlay();

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
                hideLoadingOverlay();
            } else {
                hideLoadingOverlay();
                Swal.fire("¡Ups!","Verifique que todos los datos sean correctos y los campos esten completos","error");
            }
        })
        .catch(error => {
            hideLoadingOverlay();
            console.error('Error: ' + error);
        });
    }

    loginBtn.addEventListener('click', login);
    pass.addEventListener('keypress', (e) => {
        if (e.keyCode === 13){
            login();
        }
    });

    user.addEventListener('keypress', (e) => {
        if (e.keyCode === 13){
            login();
        }
    });
});


