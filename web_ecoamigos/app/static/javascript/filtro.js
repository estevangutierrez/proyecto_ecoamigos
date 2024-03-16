document.addEventListener("DOMContentLoaded", function() {
    const inputFiltro = document.querySelector(".input-filtro input");
    const tablaMostrar = document.querySelector(".tabla-mostrar");
    const filasUsuarios = tablaMostrar.querySelectorAll("tr"); // Obtenemos todas las filas de usuarios
    
    inputFiltro.addEventListener("input", function() {
        const filtro = inputFiltro.value.trim().toLowerCase(); // Obtenemos el valor del filtro en minúsculas
        
        // Iteramos sobre las filas de usuarios y mostramos solo las que coincidan con el filtro
        filasUsuarios.forEach(function(fila) {
            const idUsuario = fila.querySelector("td:first-child").textContent.toLowerCase(); // Obtenemos el ID del usuario en la primera columna
            if (idUsuario.includes(filtro)) {
                fila.style.display = ""; // Mostramos la fila si coincide con el filtro
            } else {
                fila.style.display = "none"; // Ocultamos la fila si no coincide con el filtro
            }
        });
    });
});
