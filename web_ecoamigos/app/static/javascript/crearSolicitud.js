const actionButton = document.getElementById('enviar-btn');


actionButton.addEventListener('click', (e) => {
    e.preventDefault()
    let cantidad = document.getElementById('cantidad-aceite').value
    let detalle = document.getElementById('observaciones').value
    const dialog = document.querySelector('#contenedor-emergente')

    if (cantidad.trim() === ''){
        dialog.close()
        Swal.fire('Campo vacío','Ingrese una cantidad aproximada','warning');
        return;
    }

    const formData = {
        cantidad:cantidad,
        detalle:detalle
    }

    fetch('/proveedor/enviar_solicitud', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json' 
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {

        dialog.close()

        if(data.ok){
            console.log(data.ok)
            Swal.fire('Genial','Solicitud enviada exitosamente','success')
        } else if(data.existe){
            Swal.fire('Ups','No puedes enviar esta solicitud porque ya tienes una solicitud en proceso','warning')
        } else if(data.error){
            Swal.fire('Ups','Ha ocurrido un error','error')
        }

    })
    .catch(error => {
        console.error("Ha ocurrido un error", error)
        Swal.fire('Ups','Ha ocurrido un error','error')   
    })
    
})