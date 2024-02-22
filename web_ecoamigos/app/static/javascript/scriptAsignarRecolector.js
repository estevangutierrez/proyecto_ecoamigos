document.addEventListener('DOMContentLoaded', function () {

    const selectAll = document.getElementById('selectAllCheck');

    selectAll.addEventListener('change', () => {
        const checkBoxes = document.querySelectorAll('.tabla-mostrar input[type="checkbox"]');
        checkBoxes.forEach(checkBox => {
            if(checkBox.checked){
                checkBox.checked = false;
            } else {
                checkBox.checked = true;
            }
        });
    })


    const asignarButton = document.getElementById('asignar-rec');
    const loadingOverlay = document.getElementById('loadingOverlay');

    asignarButton.addEventListener('click', function () {
        const filasSeleccionadas = document.querySelectorAll('.tabla-mostrar input[type="checkbox"]:checked');
        const idRecolector = document.getElementById('reco-select').value;

        if (idRecolector == 'null') {
            Swal.fire('Ojito', 'Debes seleccionar un recolector', 'error');
            return;
        }

        const idNumericoRecolector = idRecolector ? parseInt(idRecolector.match(/\d+/)[0]) : null;
        const datos = {};
        const recolector = {id_recolector:idNumericoRecolector};
        datos.recolector = recolector;
        const solicitudes = {};
        const solicitudes_list = [];

        filasSeleccionadas.forEach(fila => {
            const idSolicitud = fila.closest('tr').querySelector('td:first-child').textContent;
            solicitudes_list.push({id_solicitud:idSolicitud})
        });

        solicitudes.solicitudes = solicitudes_list;
        datos.solicitudes = solicitudes;

        Swal.fire({
            title: "¿Estás seguro?",
            text: "Asignarás todas las solicitudes marcadas",
            icon: "warning",
            showCancelButton: true,
            confirmButtonColor: "#3085d6",
            cancelButtonText: 'Cancelar',
            cancelButtonColor: "#d33",
            confirmButtonText: "Sí, asignar"
        }).then((result) => {
            if (result.isConfirmed) {
                // Mostrar el overlay
                loadingOverlay.style.display = 'block';

                // Llamar a la función para asignar recolector
                asignarRecolector(datos);
            }
        });
    });

    function asignarRecolector(datos) {
        fetch('/administrador/solicitudes/asignar', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(datos)
        })
            .then(response => response.json())
            .then(data => {
                // Ocultar el overlay después de completar la llamada
                loadingOverlay.style.display = 'none';

                // Mostrar el mensaje de Swal
                Swal.fire(data.mensaje, '', data.icono);
            })
            .catch(error => {
                // Ocultar el overlay en caso de error
                loadingOverlay.style.display = 'none';

                // Mostrar mensaje de error de Swal
                Swal.fire('Error al asignar', error, 'error');
            });
    }
});
