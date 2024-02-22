const tokenButton = document.getElementById('tokens-btn');
const tokenWindow = document.getElementById('contenedor-token');


tokenButton.addEventListener('click', () => {
    tokenWindow.showModal();
});

const closeButton = document.getElementById('cerrar-token');
closeButton.addEventListener('click', () => {
    tokenWindow.close()
})