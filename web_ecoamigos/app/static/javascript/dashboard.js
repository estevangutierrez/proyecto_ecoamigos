document.addEventListener("DOMContentLoaded", function(){
const dialog = document.querySelector('#contenedor-emergente');
const solicitaRecolecta = document.querySelector('#solicitador-recolecta');
const botonCerrar = document.querySelector('#boton-cerrar');

console.log(solicitaRecolecta);

solicitaRecolecta.addEventListener('click', () => {
    dialog.showModal();
});

botonCerrar.addEventListener('click', () => {
    dialog.close();
});
});