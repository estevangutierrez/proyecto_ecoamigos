document.addEventListener("DOMContentLoaded", function () {

    const btnRegistrar = document.querySelector(".nuevo-usuario");
    const btnCerrar = document.getElementById("btn-cerrar");
    const formularioEmergente = document.getElementById("formulario-emergente");
    const background = document.getElementById("fondo-oscuro");

    const cerrarVentana = () => {
        document.getElementsByTagName('input').value = ''
    
        background.style.display = 'none';
        formularioEmergente.style.display = 'none';
    }

    btnRegistrar.addEventListener("click", function () {
        formularioEmergente.style.display = "block";
        background.style.display = "block";
    });

    background.addEventListener("click", cerrarVentana);

    btnCerrar.addEventListener("click", cerrarVentana);
});

