document.addEventListener('DOMContentLoaded', function() {
    const btnBuscar = document.getElementById('btn-buscar-filtro');

    btnBuscar.addEventListener('click', function() {
        const fechaFiltro = document.getElementById('filtro-fecha').value;
        const publicaciones = document.querySelectorAll('#publicaciones-cont tr');

        // Iterar sobre cada fila de la tabla de publicaciones
        publicaciones.forEach(function(publicacion) {
            const fechaPublicacion = publicacion.querySelector('td:nth-child(3)').textContent;
            
            // Comparar la fecha de la publicación con la fecha seleccionada en el filtro
            if (fechaFiltro === fechaPublicacion) {
                publicacion.style.display = ''; // Mostrar la fila si coincide con la fecha del filtro
            } else {
                publicacion.style.display = 'none'; // Ocultar la fila si no coincide con la fecha del filtro
            }
        });
    });
});
