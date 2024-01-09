document.addEventListener('DOMContentLoaded', () => {

    const cerrarVentana = () => {
        const formulario = document.getElementById('formulario-emergente');
        const background = document.getElementById('fondo-oscuro');
    
        document.getElementById('nombre').value = '';
        document.getElementById('correo').value = '';
        document.getElementById('telefono').value = '';
        document.getElementById('id').value = '';
    
        background.style.display = 'none';
        formulario.style.display = 'none';
    }
        
    document.getElementById('btn-cerrar').addEventListener('click', cerrarVentana)

    function cargarAdministradores(){
        fetch('/cargar_administradores')
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
        const tablaAdmin = document.getElementById('admin-tabla')
        // Limpiar la tabla existente
        tablaAdmin.innerHTML = "";

        // Construir la tabla con los datos recibidos
        data.forEach(admin => {
            const row = document.createElement('tr');
            
            const id = document.createElement('td');
            const nombre = document.createElement('td');
            const correo = document.createElement('td');
            const telefono = document.createElement('td');
            const estado = document.createElement('td');
            
            id.innerText = admin.id;
            nombre.innerText = admin.nombre;
            correo.innerText = admin.correo;
            telefono.innerText = admin.celular;
            if(admin.estado == true){
                estado.innerText = 'ACTIVO'
            } else {
                estado.innerText = 'INACTIVO'
            }

            row.appendChild(id);
            row.appendChild(nombre);
            row.appendChild(correo);
            row.appendChild(telefono);
            row.appendChild(estado);

            tablaAdmin.appendChild(row)
        });
    }

    cargarAdministradores()

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
                cerrarVentana()
                cargarAdministradores()
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
