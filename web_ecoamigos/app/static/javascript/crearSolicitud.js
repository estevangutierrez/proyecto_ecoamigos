const actionButton = document.getElementById('enviar-btn');


actionButton.addEventListener('click', (e) => {
    e.preventDefault()
    let cantidad = document.getElementById('cantidad-aceite').value
    let detalle = document.getElementById('detalle').value

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
        console.log(data.mensaje)
        alert('Solicitud enviada con exito')
    })
    .catch(error => {
        console.error("Ha ocurrido un error", error)
    })
    
})