document.addEventListener('DOMContentLoaded', ()=> {
    const id = document.getElementById('documento');
    const correo = document.getElementById('correo');

    const enviarButton = document.getElementById('enviar');

    const Toast = Swal.mixin({
        toast: true,
        position: "top",
        showConfirmButton: false,
        timer: 3000,
        timerProgressBar: true,
        didOpen: (toast) => {
          toast.onmouseenter = Swal.stopTimer;
          toast.onmouseleave = Swal.resumeTimer;
        }
      })

    const loadingOverlay = document.getElementById('loadingOverlay');


    function showLoadingOverlay() {
        loadingOverlay.style.display = 'block';
    }
  
    function hideLoadingOverlay() {
        loadingOverlay.style.display = 'none';
    }


    function recuperarContrasena() {
        data = {
            id:id.value,
            correo:correo.value
        };

        fetch('/recuperar_contrasena', {
            method: 'PUT',
            headers: {
                'Content-Type':'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            hideLoadingOverlay()
            Toast.fire({
                'icon':data.icono,
                'title':data.mensaje
            });

            document.getElementById('documento').value = '';
            document.getElementById('correo').value = '';
        })
        .catch(error => {
            console.log(error)
            Toast.fire({
                'icon':'error',
                'title':'Hubo un error en la solicitud'
            });
        })
    };


    enviarButton.addEventListener('click', (e) => {
        e.preventDefault();
        showLoadingOverlay();
        recuperarContrasena();
    });
})