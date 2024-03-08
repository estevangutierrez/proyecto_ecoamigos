document.addEventListener('DOMContentLoaded', ()=> {

    function recargarPagina(tiempo) {
        setTimeout(function() {
            location.reload();
        }, tiempo);
    } 

    function enviarJSON(json,ruta){
        fetch(ruta, {
            method : 'PUT',
            headers : {
                'Content-Type' : 'application/json'
            },
            body : JSON.stringify(json)
        })
        .then(response => response.json())
        .then(data => {
            Swal.fire(data.mensaje,'',data.icono);
            recargarPagina(3000);
        })
        .catch(error => console.log(error))
    }

    const realizarCanjeo = document.querySelectorAll('.adm-canjear-btn');

    realizarCanjeo.forEach(button => {
        button.addEventListener('click', async () => {
            const idCanjeo = button.value;
            console.log('id', idCanjeo)
    
            const { value: file } = await Swal.fire({
                title: "Comprobante",
                input: "file",
                inputAttributes: {
                  "accept": "image/*",
                  "aria-label": "Sube aqui el comprobante de pago"
                }
              });
              if (file) {
                const reader = new FileReader();
                reader.onload = (e) => {
                  Swal.fire({
                    title: "Verifica que sea el comprobante correcto",
                    imageUrl: e.target.result,
                    imageAlt: "Imagen del comprobante"
                  })
                  .then((result) => {
                        if (result.isConfirmed) {
                            const datos = {
                                imagenURL: e.target.result,
                                id_canjeo: idCanjeo
                            }
                            enviarJSON(datos, '/administrador/canjeos/confirmar_canjeo');
                        } 
                   })
                   .catch(error => console.log(error))
                };
    
                reader.readAsDataURL(file);
              } else {
                Swal.fire('Por favor, carga el comprobante','','warning')
              }
        })
            
        });
})