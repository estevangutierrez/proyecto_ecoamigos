document.addEventListener('DOMContentLoaded', () => {

    function cargarRecolectores(){
        fetch('/cargar_recolectores')
        .then(response => {
            if(!response.ok){
                console.error('La respuesta no fue recibida correctamente')
            }
            return response.json();
        })
        .then(data => {
            actualizarTabla(data);        
        });
    }

    function actualizarTabla(data) {
        const tablaRecolector = document.getElementById('recolector-tabla')
        // Limpiar la tabla existente
        tablaRecolector.innerHTML = "";

        // Construir la tabla con los datos recibidos
        data.forEach(recolector => {
            const row = document.createElement('tr');
            
            const id = document.createElement('td');
            const nombre = document.createElement('td');
            const correo = document.createElement('td');
            const telefono = document.createElement('td');
            const comuna = document.createElement('td')
            const estado = document.createElement('td');
            
            id.innerText = recolector.id;
            nombre.innerText = recolector.nombre;
            correo.innerText = recolector.correo;
            telefono.innerText = recolector.celular;
            comuna.innerText = 'COMUNA' + recolector.comuna;
            if(recolector.estado == true){
                estado.innerText = 'ACTIVO'
            } else {
                estado.innerText = 'INACTIVO'
            }

            row.appendChild(id);
            row.appendChild(nombre);
            row.appendChild(correo);
            row.appendChild(telefono);
            row.appendChild(comuna);
            row.appendChild(estado);

            tablaRecolector.appendChild(row)
        });
    }

    cargarRecolectores()

    const cerrarVentana = () => {
        const formulario = document.getElementById('formulario-emergente');
        const background = document.getElementById('fondo-oscuro');
    
        document.getElementById('nombre').value = '';
        document.getElementById('correo').value = '';
        document.getElementById('telefono').value = '';
        document.getElementById('direccion').value = '';
        document.getElementById('comuna').value = '';
        document.getElementById('barrio').value = '';
    
        background.style.display = 'none';
        formulario.style.display = 'none';
    }
    
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
                cerrarVentana()
                cargarRecolectores()
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
    
    document.getElementById('btn-cerrar').addEventListener('click', cerrarVentana)
})