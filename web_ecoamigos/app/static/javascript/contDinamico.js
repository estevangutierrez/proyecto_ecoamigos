fetch('/blog/publicaciones')
    .then(response => response.json())
    .then(data => {
        // Iterar sobre cada noticia y mostrarla en tu HTML
        data.forEach(noticia => {
            // Crear elementos para mostrar los datos de la noticia
            const noticiaItem = document.createElement('div');
            const noticiaCont = document.createElement('div');
            const contImg = document.createElement('div');
            const tituloElement = document.createElement('h2');
            const descripcionElement = document.createElement('p');
            const imagenElement = document.createElement('img');
            const fechaElement = document.createElement('span');

            noticiaItem.classList.add('noticia-item');
            noticiaCont.classList.add('noticia-cont');
            contImg.classList.add('contenedor-imagen')
            fechaElement.classList.add('fecha');


            // Asignar datos de la noticia a los elementos
            tituloElement.innerText = noticia.titulo;
            descripcionElement.innerText = noticia.descripcion;
            descripcionElement.style.display = 'none'
            fechaElement.innerText = formatearFecha(noticia.fecha)

            imagenElement.src = `data:image/*;base64,${noticia.imagen}`


            noticiaCont.appendChild(tituloElement);
            noticiaCont.appendChild(descripcionElement);
            noticiaCont.appendChild(fechaElement);
            contImg.appendChild(imagenElement);

            noticiaItem.appendChild(contImg);
            noticiaItem.appendChild(noticiaCont);

            document.getElementById('noticias-container').appendChild(noticiaItem);

            noticiaItem.addEventListener('click', () => {
                mostrarPublicacionAmpliada(noticia);
            });
        });
    })
    .catch(error => console.error('Error:', error));

function formatearFecha(fechaString) {
    const fecha = new Date(fechaString + ' UTC-5');
    fecha.setHours(fecha.getHours());

    const options = {
        day: 'numeric',
        month: 'long',
        year: 'numeric',
        hour: 'numeric',
        minute: 'numeric',
        hour12: true
    };

    const fechaFormateada = fecha.toLocaleString('es-CO', options);
    return fechaFormateada;
}

function mostrarPublicacionAmpliada(noticia) {
    document.getElementById('titulo-publicacion').innerText = noticia.titulo;
    document.getElementById('descripcion-publicacion').innerText = noticia.descripcion;
    document.getElementById('imagen-publicacion').src = `data:image/*;base64,${noticia.imagen}`;
    document.getElementById('fecha-publicacion').innerText = formatearFecha(noticia.fecha);

    // Mostrar el diálogo
    document.getElementById('dialogo').style.display = 'block';
}

// Función para cerrar el diálogo
document.getElementById('cerrar-dialogo').addEventListener('click', () => {
    document.getElementById('dialogo').style.display = 'none';
});
