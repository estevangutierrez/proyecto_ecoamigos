document.addEventListener('DOMContentLoaded', () => {
    
    const btnAggProveedor = document.getElementById('aggProveedor');
    const loadingOverlay = document.getElementById('loadingOverlay');
    
    btnAggProveedor.addEventListener('click', (e) => {
        e.preventDefault()
    
        const id = document.getElementById('id_proveedor').value;
        const tipo = document.getElementById('tipo_proveedor').value;
        const nombre = document.getElementById('nombre_completo').value.toUpperCase();
        const correo = document.getElementById('correo').value.toUpperCase();
        const telefono = document.getElementById('celular').value;
        const direccion = document.getElementById('direccion').value.toUpperCase();
        const comuna = document.getElementById('comuna').value;
        const barrio = document.getElementById('barrio').value;
    
        if (
            id.trim() === '' ||
            nombre.trim() === '' ||
            correo.trim() === '' ||
            telefono.trim() === '' ||
            direccion.trim() === ''
        ){
            Swal.fire('Campos vacíos','Todos los campos son obligatorios','error');
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
                loadingOverlay.style.display = 'none';
                Swal.fire("¡Genial!","Usuario registrado exitosamente, su contraseña fue enviada a su correo electrónico","success");
            } else {
                loadingOverlay.style.display = 'none';
                Swal.fire("Usuario existente","Este usuario ya se encuentra registrado","error");
            }
        })
        .catch(error => {
            console.log(error)
            Swal.fire('¡Ups!','Ha ocurrido un error','error');
        })
    });
})