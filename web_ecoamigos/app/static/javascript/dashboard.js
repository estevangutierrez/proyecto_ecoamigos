document.addEventListener("DOMContentLoaded", function(){
const dialog = document.querySelector('#contenedor-emergente');
const solicitaRecolecta = document.querySelector('#solicitador-recolecta');
const botonCerrar = document.querySelector('#boton-cerrar');

solicitaRecolecta.addEventListener('click', () => {
    dialog.showModal();
});

botonCerrar.addEventListener('click', () => {
    dialog.close();
});
});