document.addEventListener('DOMContentLoaded', () => {

    function recargarPagina(tiempo) {
        setTimeout(function() {
            location.reload();
        }, tiempo);
    } 

    const Toast = Swal.mixin({
        toast: true,
        position: "top-end",
        showConfirmButton: false,
        timer: 3000,
        timerProgressBar: true,
        didOpen: (toast) => {
          toast.onmouseenter = Swal.stopTimer;
          toast.onmouseleave = Swal.resumeTimer;
        }
      });
    
    const dialog = document.getElementById('modal');
    const btnAbrirModal = document.getElementById('n-proveedor');
    const btnCerrarModal = document.getElementById('cancelar-btn');
    const btnAggProveedor = document.getElementById('aggProveedor');

    btnAbrirModal.addEventListener('click', (e) => {
        e.preventDefault();
        dialog.showModal();
    });

    btnCerrarModal.addEventListener('click', (e) =>  {
        e.preventDefault();

        const id = document.getElementById('id_proveedor');
        const tipo = document.getElementById('tipo_proveedor');
        const nombre = document.getElementById('nombre_completo');
        const correo = document.getElementById('correo');
        const correoV = document.getElementById('correo-v');
        const telefono = document.getElementById('celular');
        const direccion = document.getElementById('direccion');
        const comuna = document.getElementById('comuna');
        const barrio = document.getElementById('barrio');

        id.value = '';
        tipo.value = '';
        nombre.value = '';
        correo.value = '';
        correoV.value = '';
        telefono.value = '';
        direccion.value = '';
        comuna.value = '';
        barrio.value = '';

        dialog.close();
    })
    
    btnAggProveedor.addEventListener('click', (e) => {
        e.preventDefault()
    
        const id = document.getElementById('id_proveedor').value;
        const tipo = document.getElementById('tipo_proveedor').value;
        const nombre = document.getElementById('nombre_completo').value.toUpperCase();
        const correo = document.getElementById('correo').value.toUpperCase();
        const correoV = document.getElementById('correo-v').value.toUpperCase();
        const telefono = document.getElementById('celular').value;
        const direccion = document.getElementById('direccion').value.toUpperCase();
        const comuna = document.getElementById('comuna').value;
        const barrio = document.getElementById('barrio').value;
        const verificacionCorreo = document.getElementById('correo-v');

    
        if (
            id.trim() === '' ||
            id.length < 5 ||
            nombre.trim() === '' ||
            nombre.length < 12 ||
            correo.trim() === '' ||
            correo.length < 12 ||
            telefono.trim() === '' ||
            telefono.length < 6 ||
            direccion.trim() === '' ||
            direccion.length < 12
        ){
            Toast.fire({
                icon: "warning",
                title: "Hay campos sin completar"
              });
            return;
        } else if(correo != correoV){
            verificacionCorreo.style.borderColor = "red";
            setTimeout(function() {
                verificacionCorreo.style.borderColor = "#ccc";
            }, 6000);
            return;
        }
        
        const formData = {
            id: id,
            tipo: tipo,
            nombre: nombre,
            correo: correo,
            telefono: telefono,
            direccion: direccion,
            comuna: comuna,
            barrio: barrio
        };
    
        fetch('/nuevo_proveedor', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json' 
            },
            body: JSON.stringify(formData)
        })
        .then(response => response.json())
        .then(data => {
            if(data.success){
                document.getElementById('id_proveedor').value = '';
                document.getElementById('tipo_proveedor').value = '';
                document.getElementById('nombre_completo').value = '';
                document.getElementById('correo').value = '';
                document.getElementById('correo-v').value = '';
                document.getElementById('celular').value = '';
                document.getElementById('direccion').value = '';
                document.getElementById('comuna').value = '';
                document.getElementById('barrio').value = '';

                dialog.close()
                Swal.fire("¡Genial!","Usuario registrado exitosamente, su contraseña fue enviada a su correo electrónico","success");
                recargarPagina(3000)
            } else {
                dialog.close()
                Swal.fire("Usuario existente","Este usuario ya se encuentra registrado","error");
            }
        })
        .catch(error => {
            console.log(error)
            Toast.fire({
                icon: "error",
                title: "Ha ocurrido un error, intente nuevamente"
              });
        })
    });
})