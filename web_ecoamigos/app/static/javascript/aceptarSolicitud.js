document.addEventListener('DOMContentLoaded', () => {

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

    function recargarPagina(tiempo) {
        setTimeout(function() {
            location.reload();
        }, tiempo);
    } 

    document.getElementById('solicitudes-p-tabla').addEventListener('click', (e)=> {
        if(e.target.classList.contains('aceptar-btn')) {
            Swal.fire({
                title: "¿Deseas aceptar esta solicitud?",
                icon: "warning",
                showCancelButton: true,
                confirmButtonColor: "#3085d6",
                cancelButtonColor: "#d33",
                cancelButtonText: "No, cancelar",
                confirmButtonText: "Sí, aceptar"
            }).then((result) => {
                if (result.isConfirmed) {
                    const idSolicitud = e.target.dataset.id;
                    fetch('/recolector/aceptar_solicitud',{
                        method:'PUT',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({id_solicitud:idSolicitud})
                    })
                    .then(response => response.json())
                    .then(data => {
                        if(data.ok){
                            recargarPagina(1000)
                        } else if(data.error){
                            console.log('Error:', data.error)
                            Swal.fire('Ups',data.error,'error')
                        }
                    })
                    .catch(error=>{
                        console.error('error:',error)
                        Swal.fire('Ups','Ha ocurrido un error','error')
                    })
                }
            });
        }
    });


    const botonesConfirmar = document.querySelectorAll('#abrir-sol-btn');
    botonesConfirmar.forEach(button => {
        button.addEventListener('click', () => {
            const contenido = document.getElementById('info');
            contenido.innerHTML = ''
            const idSolicitud = button.closest('tr').cells[0].innerText;

            const cantidadAprox = parseInt(button.closest('tr').cells[6].innerText.split(',')[0]);
            const cantidadInput = document.getElementById('cantidad-aprox');
            cantidadInput.value = cantidadAprox;

            const input = document.createElement('input')
            input.setAttribute('type','text');
            input.setAttribute('disabled','true');
            input.setAttribute('id','solicitud-conf');
            input.classList.add('input-disabled');
            input.value = idSolicitud;

            contenido.appendChild(input);

            document.getElementById('dialogo-conf').showModal();
        })
    });

    const confirmarDatos = document.getElementById('confirmar-v');
    confirmarDatos.addEventListener('click', (e) => {
        e.preventDefault();
        crearJson()
    })

    function crearJson(){
        const solicitud = document.getElementById('solicitud-conf').value;
        const cantidad = document.getElementById('cantidad-aprox').value;
        const token = document.getElementById('token').value;

        if (cantidad.trim() === '' || token.trim() === ''){
            Toast.fire({
                icon: "warning",
                title: "Faltan campos por llenar"
              });
            return;
        }

        datos = {
            id_solicitud:solicitud,
            cantidad:cantidad,
            token:token
        }

        confirmarVisita(datos);
    }

    function confirmarVisita(JSONdata){        
        fetch('/recolector/solicitudes/confirmar', {
            method: 'POST',
            headers: {
                'Content-Type':'application/json'
            },
            body: JSON.stringify(JSONdata)
        })
        .then(response => response.json())
        .then(data => {            
            if(data.token_incorrecto){
                Toast.fire({
                    icon: "error",
                    title: "El token ingresado no es correcto"
                  });
                return;
            };

            document.getElementById('dialogo-conf').close();
            Swal.fire(data.mensaje,'',data.icono);
            recargarPagina(3000)
        })
        .catch(error => {
            Swal.fire('Error',error,'error')
        })
    }
})