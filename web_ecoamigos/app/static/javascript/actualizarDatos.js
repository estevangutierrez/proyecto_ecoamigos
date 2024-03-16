document.addEventListener('DOMContentLoaded', () => {


    function recargarPagina(tiempo) {
        setTimeout(function() {
            location.reload();
        }, tiempo);
    }

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
      })

    const modal = document.getElementById('actualizar-datos')
    const rolUsuario = document.getElementById('rol').innerText;
    const loadingOverlay = document.getElementById('loadingOverlay');

    function showLoadingOverlay() {
        loadingOverlay.style.display = 'block';
    }

    function hideLoadingOverlay() {
        loadingOverlay.style.display = 'none';
    }

    document.getElementById('enviar-ed').addEventListener('click', (e) => {
        e.preventDefault()

        if(rolUsuario != 'ADMINISTRADOR'){
            const cedulaN = document.getElementById('cedula').value;
            const nombreN = document.getElementById('nombre').value;
            const correoN = document.getElementById('correo').value;
            const celularN = document.getElementById('celular').value;
            const comunaN = document.getElementById('comuna').value;
            const barrioN = document.getElementById('barrio').value;
            const direccionN = document.getElementById('direccion').value;

            if(
                nombreN.trim() == '' ||
                correoN.trim() == '' ||
                celularN.trim() == '' ||
                comunaN.trim() == '' ||
                barrioN.trim() == '' ||
                direccionN.trim() == ''
            ){
                Toast.fire({
                    'icon':'warning',
                    'title':'No puedes dejar campos vacíos',
                    'position':'top-right'
                });
                return;
            }
    
            json = {
                cedula:cedulaN,
                nombre:nombreN,
                correo:correoN,
                celular:celularN,
                comuna:comunaN,
                barrio:barrioN,
                direccion:direccionN
            }
        } else {
            const cedulaN = document.getElementById('cedula').value;
            const nombreN = document.getElementById('nombre').value;
            const correoN = document.getElementById('correo').value;
            const celularN = document.getElementById('celular').value;

            if(
                nombreN.trim() == '' ||
                correoN.trim() == '' ||
                celularN.trim() == ''
            ){
                Toast.fire({
                    'icon':'warning',
                    'title':'No puedes dejar campos vacíos',
                    'position':'top-right'
                });
                return;
            }
                
            json = {
                cedula:cedulaN,
                nombre:nombreN,
                correo:correoN,
                celular:celularN
            }
        }

        console.log(json)
        enviarDatos(json, rolUsuario.toLowerCase())
    })

    
    document.getElementById('cancelar-ed').addEventListener('click', (e) => {

        e.preventDefault()

        modal.close();
        
    })

    function abrirModal() {
        if (rolUsuario !== 'ADMINISTRADOR'){

            const cedula = document.getElementById('cedula_a').innerText;
            const nombre = document.getElementById('nombre_a').innerText;
            const correo = document.getElementById('correo_a').innerText;
            const celular = document.getElementById('celular_a').innerText;
            const comuna = document.getElementById('comuna_a').innerText;
            const barrio = document.getElementById('barrio_a').innerText;
            const direccion = document.getElementById('direccion_a').innerText;

            document.getElementById('cedula').value = cedula;
            document.getElementById('nombre').value = nombre;
            document.getElementById('correo').value = correo;
            document.getElementById('celular').value = celular;
            document.getElementById('comuna').value = comuna;
            document.getElementById('barrio').value = parseInt(barrio);
            document.getElementById('direccion').value = direccion;

        } else {
            const cedula = document.getElementById('cedula_a').innerText;
            const nombre = document.getElementById('nombre_a').innerText;
            const correo = document.getElementById('correo_a').innerText;
            const celular = document.getElementById('celular_a').innerText;

            document.getElementById('cedula').value = cedula;
            document.getElementById('nombre').value = nombre;
            document.getElementById('correo').value = correo;
            document.getElementById('celular').value = celular;
        }

        modal.showModal()
    }

    document.getElementById('actualizar-datos-btn').addEventListener('click', ()=> {
        abrirModal();
    })

    function enviarDatos(JSONData, rol){
        showLoadingOverlay()

        fetch(`/${rol}/actualizar_datos`, {
            method:'PUT',
            headers: {
                'Content-Type':'application/json'
            },
            body: JSON.stringify(JSONData)
        })
        .then(response => response.json())
        .then(data => {
            console.log(data)
            modal.close()
            hideLoadingOverlay()
            Toast.fire({
                'icon':data.icono,
                'title':data.mensaje
            })
            recargarPagina(2000)
        })
        .catch(error => {
            console.log('El error fue: ', error)
            modal.close()
            hideLoadingOverlay()
            Swal.fire('Ups','Hubo un error','error')
        })
    }

    function cargarBarrios() {
        const comunaId = document.getElementById('comuna').value;
        const barrioSelect = document.getElementById('barrio');
        
        fetch(`/barrios?id_comuna=${comunaId}`)
        .then(response => response.json())
        .then(data => {
            barrioSelect.innerHTML = '';

            data.forEach(barrio => {
                const opcion = document.createElement('option');
                opcion.value = barrio.id;
                opcion.text = barrio.nombre;
                barrioSelect.appendChild(opcion) 
            });
        })
        .catch(error => console.error('Error al cargar barrios:', error));
    }

    const selectComuna = document.getElementById('comuna');
    selectComuna.addEventListener('change', cargarBarrios);
})