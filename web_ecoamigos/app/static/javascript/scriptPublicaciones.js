const botonPublicar = document.getElementById('btn-publicar');

botonPublicar.addEventListener('click', () => enviarDatos());

function enviarDatos() {
    let titulo = document.getElementById('titulo-publicacion').value;
    let descripcion = document.getElementById('contenido-publicacion').value;
    let imagen = document.getElementById('img-publicacion').files[0];

    if (
        titulo.trim() === '' ||
        descripcion.trim() === '' ||
        !imagen
    ){
        Swal.fire('Campos vacíos','Todos los campos son obligatorios','error');
        return;
    }

    const reader = new FileReader();
    reader.onload = function(e) {
        const imagenBase64 = e.target.result;

        const jsonData = {
            titulo: titulo,
            descripcion: descripcion,
            imagen: imagenBase64
        };

        enviarJSON(jsonData);
        console.log("datos-img", reader)
    };

    reader.readAsDataURL(imagen);
}

function enviarJSON(jsonData) {
    fetch('/crear_publicacion', {
        method: 'POST',
        headers: {
            'Content-Type': 'applicaton/json',
        },
        body: JSON.stringify(jsonData),
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.mensaje)
        titulo = '';
        descripcion = '';
        Swal.fire('¡Listo!','Publicación exitosa','success');
    })
    .catch(error => {
        console.log(error)
        Swal.fire('¡Ups!','Ha ocurrido un error','error'); 
    })
}

