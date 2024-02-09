document.addEventListener('DOMContentLoaded', () => {

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
                            Swal.fire('Genial',`Has aceptado la solicitud ${idSolicitud}`,'success')
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
    })
})