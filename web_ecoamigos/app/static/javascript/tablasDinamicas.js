document.addEventListener('DOMContentLoaded', function () {
    const spans = document.querySelectorAll('.menu-tablas > span');
    const tablas = document.querySelectorAll('.cont-tabla');

    // Muestra la tabla inicialmente
    tablas[0].style.display = 'block';

    spans.forEach((span, index) => {
        span.addEventListener('click', () => {
            // Oculta todas las tablas
            tablas.forEach(tabla => tabla.style.display = 'none');
            
            // Muestra solo la tabla correspondiente al índice del span clicado
            tablas[index].style.display = 'block';
        });
    });
});
