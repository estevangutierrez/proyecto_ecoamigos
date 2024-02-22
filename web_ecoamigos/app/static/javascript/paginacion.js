    document.addEventListener("DOMContentLoaded", function () {
        const itemsPerPage = 5; // Cambia esto según la cantidad de filas que quieras mostrar por página
        let currentPage = 1;
        const tableRows = document.querySelectorAll('.tabla-mostrar tr');

        const showPage = (pageNumber) => {
            const startIndex = (pageNumber - 1) * itemsPerPage;
            const endIndex = startIndex + itemsPerPage;

            tableRows.forEach((row, index) => {
                row.style.display = (index >= startIndex && index < endIndex) ? 'table-row' : 'none';
            });

            document.getElementById('currentPage').textContent = pageNumber;
        };

        const updatePage = (increment) => {
            currentPage += increment;
            if (currentPage < 1) {
                currentPage = 1;
            } else if (currentPage > Math.ceil(tableRows.length / itemsPerPage)) {
                currentPage = Math.ceil(tableRows.length / itemsPerPage);
            }

            showPage(currentPage);
        };

        document.getElementById('prevPage').addEventListener('click', () => updatePage(-1));
        document.getElementById('nextPage').addEventListener('click', () => updatePage(1));

        // Mostrar la primera página al cargar la página
        showPage(currentPage);
    });
