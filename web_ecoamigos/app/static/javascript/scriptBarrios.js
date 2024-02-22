document.addEventListener('DOMContentLoaded', () => {

    function cargarBarrios() {
        const comunaId = document.getElementById('comuna').value;
        const barrioSelect = document.getElementById('barrio');
        
        fetch(`/barrios?id_comuna=${comunaId}`)
        .then(response => response.json())
        .then(data => {
            barrioSelect.innerHTML = '';

            data.forEach(barrio => {
                const opcion = document.createElement('option');
                opcion.value = barrio.id;
                opcion.text = barrio.nombre;
                barrioSelect.appendChild(opcion) 
            });
        })
        .catch(error => console.error('Error al cargar barrios:', error));
    }

    const selectComuna = document.getElementById('comuna');
    selectComuna.addEventListener('change', cargarBarrios);
})