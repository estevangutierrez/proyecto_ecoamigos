document.addEventListener('DOMContentLoaded', () => {
    const abrirModal = document.getElementById('cambiar-contrasena-btn');
    const cerrarModal = document.getElementById('cancelar-c');
    const modal = document.getElementById('cambiar-contrasena');
    const enviarDatos = document.getElementById('enviar-c');

    const idUusario = document.getElementById('id-usuario')
    const contrasenaActual = document.getElementById('contrasena_a');
    const contrasenaNueva = document.getElementById('contrasena_n');
    const contrasenaNuevaB = document.getElementById('check_c');

    const loadingOverlay = document.getElementById('loadingOverlay');

    function limpiarFormulario() {
        contrasenaActual.value = '';
        contrasenaNueva.value = '';
        contrasenaNuevaB.value = '';

        contrasenaNueva.style.borderColor = '#ccc';
        contrasenaNuevaB.style.borderColor = '#ccc';
    }

    function showLoadingOverlay() {
        loadingOverlay.style.display = 'block';
    }

    function hideLoadingOverlay() {
        loadingOverlay.style.display = 'none';
    }

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


    function verificarNuevaContrasena(contra_a,contra_b){
        if(contra_a.value != contra_b.value ){
            return false
        } else {
            return true
        }
    }

    function cambiarContrasena(){
        showLoadingOverlay()

        data = {
            id_usuario : idUusario.value,
            contrasena_actual : contrasenaActual.value,
            contrasena_nueva : contrasenaNueva.value
        }

        fetch('/cambiar_contrasena', {
            method: 'PUT',
            headers : {
                'Content-Type':'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            limpiarFormulario();
            modal.close();
            hideLoadingOverlay();
            Toast.fire({
                'icon': data.icono,
                'title': data.mensaje
            });
        })
        .catch(error => {
            modal.close();
            hideLoadingOverlay();
            Toast.fire({
                'icon':'error',
                'title':'Hubo un error. Intenta nuevamente'
            });
            console.error(error);
        })
    }



    abrirModal.addEventListener('click', (e) => {
        e.preventDefault();
        modal.showModal();
    });

    cerrarModal.addEventListener('click', (e) => {
        e.preventDefault();

        document.getElementById('contrasena_a').value = '';
        document.getElementById('contrasena_n').value = '';
        document.getElementById('check_c').value = '';

        modal.close();
    });


    enviarDatos.addEventListener('click', (e) => {
        e.preventDefault();

        isPassOk = verificarNuevaContrasena(contrasenaNueva, contrasenaNuevaB);

        if(!isPassOk){
            Toast.fire({
                'icon':'warning',
                'title':'La contraseña nueva no coincide en ambos campos'
            });

            contrasenaNueva.style.borderColor = 'red';
            contrasenaNuevaB.style.borderColor = 'red';

            return;
        }

        contrasenaNueva.style.borderColor = 'green';
        contrasenaNuevaB.style.borderColor = 'green';

        cambiarContrasena();
    })

})