document.addEventListener('DOMContentLoaded', () => {
    const btnAggAdmin = document.getElementById('aggAdmin');
    const loadingOverlay = document.getElementById('loadingOverlay');

    btnAggAdmin.addEventListener('click', (e) => {
        e.preventDefault()
    
        const nombre = document.getElementById('nombre').value.toUpperCase();
        const correo = document.getElementById('correo').value.toUpperCase();
        const telefono = document.getElementById('telefono').value;
        const id = document.getElementById('id').value;
    
        if (
            id.trim() === '' ||
            nombre.trim() === '' ||
            correo.trim() === '' ||
            telefono.trim() === ''
        ){
            Swal.fire('Campos vacíos','Todos los campos son obligatorios','error');
            return;
        }
    
        loadingOverlay.style.display = 'flex';
    
        const formData = {
            id: id,
            nombre: nombre,
            correo: correo,
            telefono: telefono
        };
    
        fetch('/nuevo_administrador', {
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
                Swal.fire("¡Genial!","Usuario registrado exitosamente","success");
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