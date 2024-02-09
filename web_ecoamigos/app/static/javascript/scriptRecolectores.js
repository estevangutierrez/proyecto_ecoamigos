document.addEventListener('DOMContentLoaded', () => {
    
    const btnAggRecolector = document.getElementById('aggRecolector');
    const loadingOverlay = document.getElementById('loadingOverlay');
    
    btnAggRecolector.addEventListener('click', (e) => {
        e.preventDefault()
    
        const id = document.getElementById('id').value;
        const nombre = document.getElementById('nombre').value.toUpperCase();
        const correo = document.getElementById('correo').value.toUpperCase();
        const telefono = document.getElementById('telefono').value;
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
            nombre: nombre,
            correo: correo,
            telefono: telefono,
            direccion: direccion,
            comuna: comuna,
            barrio: barrio
        };
    
        fetch('/nuevo_recolector', {
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
            loadingOverlay.style.display = 'none';
        })
    });
})