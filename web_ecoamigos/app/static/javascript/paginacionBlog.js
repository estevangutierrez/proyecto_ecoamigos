document.addEventListener("DOMContentLoaded", function () {
    const itemsPerPage = 12; // Cambia esto según la cantidad de filas que quieras mostrar por página
    let currentPage = 1;
    const noticias = document.querySelectorAll('.noticias-container .noticia-item');

    const showPage = (pageNumber) => {
        const startIndex = (pageNumber - 1) * itemsPerPage;
        const endIndex = startIndex + itemsPerPage;

        noticias.forEach((row, index) => {
            row.style.display = (index >= startIndex && index < endIndex) ? 'flex' : 'none';
        });

        document.getElementById('currentPage').textContent = pageNumber;
    };

    const updatePage = (increment) => {
        currentPage += increment;
        if (currentPage < 1) {
            currentPage = 1;
        } else if (currentPage > Math.ceil(noticias.length / itemsPerPage)) {
            currentPage = Math.ceil(noticias.length / itemsPerPage);
        }

        showPage(currentPage);
    };

    document.getElementById('prevPage').addEventListener('click', () => updatePage(-1));
    document.getElementById('nextPage').addEventListener('click', () => updatePage(1));

    // Mostrar la primera página al cargar la página
    showPage(currentPage);
});