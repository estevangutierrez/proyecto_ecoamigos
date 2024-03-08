// Supongamos que después de cerrar sesión, rediriges al index
const urlDelIndex = "http://127.0.0.1:5000/"; // Ajusta la URL según tu estructura de archivos

function cerrarSesion() {
    // Realizar lógica de cierre de sesión aquí
    window.location.replace(urlDelIndex);
    window.history.replaceState({}, document.title, urlDelIndex);
}

// Manejar el evento popstate para detectar cambios en el historial
window.addEventListener('popstate', function (event) {
    // Verificar si la página actual es la página de cierre de sesión y redirigir al índice
    if (window.location.pathname !== urlDelIndex) {
        window.location.replace(urlDelIndex);
        window.history.replaceState({}, document.title, urlDelIndex);
    }
});

document.getElementById('cerrar-s').addEventListener('click', ()=> {
    cerrarSesion();
})
