document.addEventListener('DOMContentLoaded', ()=> {

    const loadingOverlay = document.getElementById('loadingOverlay');

    function showLoadingOverlay() {
        loadingOverlay.style.display = 'block';
    }

    function hideLoadingOverlay() {
        loadingOverlay.style.display = 'none';
    }

    function verComprobante(id){
        showLoadingOverlay()
        fetch(`/proveedor/mis_canjeos/soporte/${id}`)
        .then(response => response.json())
        .then(data => {
            hideLoadingOverlay()
            Swal.fire({
                title: "Este es el comprobante de pago de tu canjeo",
                text: "*Si no ves reflejado este pago en tu cuenta, comunicate con nosotros.",
                imageUrl: `data:image/*;base64,${data.imagen}`,
                imageWidth: 370,
                imageHeight: 789,
                imageAlt: "Comprobante"
              });
        })
        .catch(error => console.error(error))
    }

    const botones = document.querySelectorAll('.btn-comprobante');

    botones.forEach(boton => {
        boton.addEventListener('click', (e)=> {
            const id_comprobante = e.target.value;
            console.log('EL COMPROBANTE ES', id_comprobante)
            verComprobante(id_comprobante);
        })
    })
})