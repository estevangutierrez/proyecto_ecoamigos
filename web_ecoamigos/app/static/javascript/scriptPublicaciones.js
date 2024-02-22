// Publicar
const botonPublicar = document.getElementById('btn-publicar');
botonPublicar.addEventListener('click', publicar);

async function publicar(e) {
    e.preventDefault();
    const titulo = document.getElementById('titulo-publicacion').value;
    const descripcion = document.getElementById('contenido-publicacion').value;
    const imagen = document.getElementById('img-publicacion').files[0];

    if (titulo.trim() === '' || descripcion.trim() === '' || !imagen) {
        mostrarError('Campos vacíos', 'Todos los campos son obligatorios');
        return;
    }

    const imagenBase64 = await convertirImagenBase64(imagen);

    const jsonData = {
        titulo: titulo,
        descripcion: descripcion,
        imagen_data: imagenBase64
    };

    await enviarJSON(jsonData);
    console.log("datos_img", imagenBase64);
}

function mostrarError(title, message) {
    Swal.fire(title, message, 'error');
}

async function convertirImagenBase64(imagen) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(imagen);
        reader.onload = function (e) {
            resolve(e.target.result);
        };
        reader.onerror = function (error) {
            reject(error);
        };
    });
}

async function enviarJSON(jsonData) {
    try {
        const response = await fetch('/crear_publicacion', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(jsonData),
        });

        const data = await response.json();
        console.log(data.mensaje);
        mostrarMensaje(data.mensaje);

    } catch (error) {
        console.log(error);
        mostrarError('¡Ups!', 'Ha ocurrido un error');
    }
}

function mostrarMensaje(message,icono) {
    Swal.fire('', message,icono);
}

// Editar
const enviarEditado = document.getElementById('enviar-ed');
enviarEditado.addEventListener('click', actualizarPublicacion);

const cancelarEditado = document.getElementById('cancelar-ed');
cancelarEditado.addEventListener('click', cerrarModal);

let filaActual; // Variable para almacenar la fila actualmente editada

function editarPublicacion(event) {
    const botonEditar = event.currentTarget;
    const filaActual = botonEditar.closest('tr');
    const id = filaActual.cells[0].innerText;

    const titulo = filaActual.cells[1].innerText;
    const descripcion = filaActual.cells[2].innerText;

    document.getElementById('id-active').value = id;
    document.getElementById('titulo-ed').value = titulo;
    document.getElementById('descripcion-ed').value = descripcion;
    document.getElementById('img-ed').value = '';

    document.getElementById('modal').showModal();

    console.log('ID de la fila actual:', id);
}

function eliminarPublicacion(event) {
    const botonEliminar = event.currentTarget;
    const filaActual = botonEliminar.closest('tr');
    const id = filaActual.cells[0].innerText;

    Swal.fire({
        title: "¿Estás seguro?",
        text: "La publicaciones eliminadas no se pueden revertir",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonText: 'Cancelar',
        cancelButtonColor: "#d33",
        confirmButtonText: "Sí, eliminar"
      }).then((result) => {
        if (result.isConfirmed) {
            fetch(`/publicaciones/eliminar/${id}`, {
                method: 'DELETE'
            })
            .then(response => response.json())
            .then(data => {
                Swal.fire({
                    text: data.mensaje,
                    icon: data.icono
                  });
            })
            .catch(error => {
                mostrarError('Error al eliminar',error);
            })
        }
      });

}

function cerrarModal() {
    document.getElementById('modal').close();
}

function actualizarPublicacion() {
    const id = document.getElementById('id-active').value;
    const nuevoTitulo = document.getElementById('titulo-ed').value;
    const nuevaDescripcion = document.getElementById('descripcion-ed').value;
    const imagenBlob = document.getElementById('img-ed').files[0];

    let imagen;

    if (imagenBlob){
        convertirImagenBase64(imagenBlob)
        .then((imagenBase64) => {
            imagen = imagenBase64;
            enviarPeticionEditar(id,nuevoTitulo,nuevaDescripcion,imagen)
        })
        .catch((error) => {
            console.error(error)
        })
    } else {
        enviarPeticionEditar(id,nuevoTitulo,nuevaDescripcion);
    }
}

function enviarPeticionEditar(id,titulo,descripcion,imagen=null){
    cerrarModal();
    fetch(`/publicaciones/editar/${id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            titulo: titulo,
            descripcion: descripcion,
            imagen: imagen
        })
    })
    .then(response => response.json())
    .then(data => {
        mostrarMensaje(data.mensaje,data.icono);
    })
    .catch(error => {
        mostrarError('Error al editar',error);
    });
}

// Modificar la asignación del evento para usar la nueva función editarPublicacion
const editarButtons = document.querySelectorAll('.editar');
editarButtons.forEach(button => {
    button.addEventListener('click', editarPublicacion);
});

const eliminarButtons = document.querySelectorAll('.eliminar');
eliminarButtons.forEach(button => {
    button.addEventListener('click', eliminarPublicacion);
})


