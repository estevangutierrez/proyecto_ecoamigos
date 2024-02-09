document.addEventListener('DOMContentLoaded', () => {
    
    const btnAggProveedor = document.getElementById('aggProveedor');
    const loadingOverlay = document.getElementById('loadingOverlay');
    
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
            Swal.fire('Campos vacíos','Todos los campos son obligatorios','error');
            return;
        } else if(correo != correoV){
            verificacionCorreo.style.borderColor = "red";
            setTimeout(function() {
                verificacionCorreo.style.borderColor = "#ccc";
            }, 6000);
            return;
        }
    
        loadingOverlay.style.display = 'flex';
    
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
                document.getElementById('formulario-emergente').style.display = "none";
                document.getElementById('fondo-oscuro').style.display = "none"
                loadingOverlay.style.display = 'none';

                Swal.fire("¡Genial!","Usuario registrado exitosamente, su contraseña fue enviada a su correo electrónico","success");
            } else {
                loadingOverlay.style.display = 'none';
                Swal.fire("Usuario existente","Este usuario ya se encuentra registrado","error");
            }
        })
        .catch(error => {
            console.log(error)
            loadingOverlay.style.display = 'none';
            Swal.fire('¡Ups!','Ha ocurrido un error','error');
        })
    });
})

