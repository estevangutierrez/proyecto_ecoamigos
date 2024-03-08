document.addEventListener('DOMContentLoaded', () => {
    const fechaActual = new Date();
    const diaSemana = fechaActual.getDay();
    const puntosActuales = document.getElementById('puntos-activos').innerText;
    const dialog = document.getElementById('form-canjeo');
    const solicitarCanjeo = document.getElementById('btn-solicitar-canjeo');
    const enviarDatos = document.getElementById('enviar');
    
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

    function enviarJSON(json,ruta){
        fetch(ruta, {
            method : 'POST',
            headers : {
                'Content-Type' : 'application/json'
            },
            body : JSON.stringify(json)
        })
        .then(response => response.json())
        .then(data => {
            dialog.close()
            Swal.fire(data.mensaje,'',data.icono);
            recargarPagina(3000)
        })
        .catch(error => console.log(error))
    }

    function obtenerDatosBancarios(){

        const banco = document.getElementById('banco').value;
        const cuenta = document.getElementById('cuenta').value;
        console.log(banco)
        if(banco == 'none'){
            Toast.fire({
                icon: "warning",
                title: "Selecciona un banco o medio de pago"
              });
            return;
        }
        
        dialog.close();

        Swal.fire({
            title: "¿Cuántos puntos deseas canjear?",
            icon: "question",
            input: "range",
            inputLabel: "Puntos",
            inputAttributes: {
                min: 200,
                max: puntosActuales,
                step: 5
            },
            inputValue: puntosActuales,
            showCancelButton: true,
            confirmButtonText: "Canjear",
            cancelButtonText: "Cancelar"
        }).then((result) => {
            if (result.isConfirmed) {
                const puntos = result.value;
                datos = {
                    banco:banco,
                    cuenta:cuenta,
                    puntos:puntos
                }

                enviarJSON(datos,'/proveedor/canjear_puntos')

            } else {
                return;
            }
        });

        document.getElementById('banco').value = '';
        document.getElementById('cuenta').value = '';
    }

    solicitarCanjeo.addEventListener('click',() => {
        diasValidos = [1,2,3,5]
        if(!diasValidos.includes(diaSemana)){
            Swal.fire('Dia incorrecto','solo puedes canjear de lunes a miercoles','warning');
            return;
        } else if(puntosActuales < 200){
            Swal.fire('Pocos puntos','','error');
            return;
        }

        dialog.showModal();
    })

    enviarDatos.addEventListener('click', () => {
        obtenerDatosBancarios()
    })

    document.getElementById('cancelar-btn').addEventListener('click', (e) => {
        e.preventDefault();
        dialog.close();
    })


})