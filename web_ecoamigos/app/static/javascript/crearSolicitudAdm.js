const enviarDatos = document.getElementById('enviar-solicitud');
const abrirModalBtn = document.getElementById('formulario-sol');
const cerrarModal = document.getElementById('cancelar-env');
var dialog = document.querySelector('#modal');

abrirModalBtn.addEventListener('click', (e)=> {
    e.preventDefault()
    dialog.showModal();
});

cerrarModal.addEventListener('click', (e) => {
    e.preventDefault()
    let proveedor = document.getElementById('proveedor-id');
    let cantidad = document.getElementById('cantidad-aceite');
    let detalle = document.getElementById('detalle');

    proveedor.value = '';
    cantidad.value  = '';
    detalle.value = '';

    dialog.close();
})

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

function recargarPagina() {
    setTimeout(function() {
        location.reload();
    }, 3000);
}



enviarDatos.addEventListener('click', (e) => {
    e.preventDefault()
    let proveedor = document.getElementById('proveedor-id').value;
    let cantidad = document.getElementById('cantidad-aceite').value
    let detalle = document.getElementById('detalle').value

    if (cantidad.trim() === ''){
        Toast.fire({
            icon: "warning",
            title: "Faltan campos por llenar"
          });
        return;
    }

    const formData = {
        proveedor:proveedor,
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
        if(data.ok){
            dialog.close()
            Swal.fire('Genial','Solicitud creada exitosamente','success')
            recargarPagina()
        } else if(data.existe){
            dialog.close()
            Swal.fire('Ups','Este proveedor ya tiene una solicitud en proceso','warning')
        } else if(data.error){
            Toast.fire({
                icon: "error",
                title: "Ha ocurrido un error, intenta nuevamente"
              });
        }
    })
    .catch(error => {
        console.error("Ha ocurrido un error", error)
        dialog.close()
        Swal.fire('Ups','Ha ocurrido un error, intenta nuevamente','error')   
    })
    
})