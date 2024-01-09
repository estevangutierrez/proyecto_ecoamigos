document.addEventListener("DOMContentLoaded", function () {
    const btnRegistrar = document.querySelector(".nuevo-usuario");

    const formularioEmergente = document.getElementById("formulario-emergente");
    const fondoOscuro = document.getElementById("fondo-oscuro");

    btnRegistrar.addEventListener("click", function () {
        formularioEmergente.style.display = "block";
        fondoOscuro.style.display = "block";
    });

    fondoOscuro.addEventListener("click", function () {
        formularioEmergente.style.display = "none";
        fondoOscuro.style.display = "none";
    })
});

