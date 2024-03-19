document.addEventListener('DOMContentLoaded', () => {

    const loadingOverlay = document.getElementById('loadingOverlay');

    function showLoadingOverlay() {
        loadingOverlay.style.display = 'block';
    };

    function hideLoadingOverlay() {
        loadingOverlay.style.display = 'none';
    };

    function recargarPagina(tiempo) {
        setTimeout(function() {
            location.reload();
        }, tiempo);
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
    });


    function enviarPeticion(accion, datos){
        showLoadingOverlay();
        fetch(`/usuarios/${accion}`, {
            method: 'PUT',
            headers: {
                'Content-Type':'application/json'
            },
            body: JSON.stringify(datos)
        })
        .then(response => response.json())
        .then(data => {
            hideLoadingOverlay();
            Toast.fire({
                'icon':data.icono,
                'title':data.mensaje
            });
            recargarPagina(3000);
        })
        .catch(error => {
            Toast.fire({
                'icon':'error',
                'title':'Hubo un error. Intenta nuevamente'
            })
            console.log(error);
        })
    }

    const botones = document.querySelectorAll('.ed-del');
    botones.forEach(boton => {
        boton.addEventListener('click', (e)=> {
            const currentUserId = document.getElementById('currentUser');
            const botonDesactivar = e.currentTarget;
            const filaActual = botonDesactivar.closest('tr');
            const id = filaActual.cells[0].innerText;

            if(id == currentUserId){
                Toast.fire({
                    'icon':'error',
                    'title':'No puedes desactivar tu propio usuario'
                });
                return;
            }

            console.log(id);

            datos = {
                id:id
            };

            Swal.fire({
                title: "¿Estás seguro?",
                text: "Esta acción es reversible. Puedes reactivar este usuario nuevamente.",
                icon: "warning",
                showCancelButton: true,
                confirmButtonColor: "#3085d6",
                cancelButtonText: 'Cancelar',
                cancelButtonColor: "#d33",
                confirmButtonText: "Desactivar"
              }).then((result) => {
                if (result.isConfirmed) {
                    enviarPeticion('desactivar',datos);
                }
              });
        });
    });

})