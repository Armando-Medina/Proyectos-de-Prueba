let editandoId = null; 

document.getElementById('form-registro').addEventListener('submit', async (e) => {
    e.preventDefault();

    const datosJugador = {
        nombre: document.getElementById('nombre').value,
        apellido: document.getElementById('apellido').value,
        fecha_nacimiento: document.getElementById('fecha_nacimiento').value,
        telefono: document.getElementById('telefono').value,
        correo: document.getElementById('correo').value,
        direccion: document.getElementById('direccion').value,
        posicion: document.getElementById('posicion').value,   
        pie_dominante: document.getElementById('pie_dominante').value,
        altura: parseFloat(document.getElementById('altura').value) || 0,
        peso: parseFloat(document.getElementById('peso').value) || 0
    };

    const url = editandoId
        ? `http://127.0.0.1:5000/editar/${editandoId}`
        : 'http://127.0.0.1:5000/registrar';

    const metodo = editandoId ? 'PUT' : 'POST';

    try {
        const respuesta = await fetch(url, {
            method: metodo,
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(datosJugador)
        });

        const resultado = await respuesta.json();
        const mensajeDiv = document.getElementById('mensaje-respuesta');

        if (respuesta.ok) {
            mensajeDiv.innerHTML = `<p style="color: green;">✅ ${resultado.mensaje}</p>`;

            editandoId = null;
            document.getElementById('btn-registrar').innerText = "Registrar Jugador";
            document.getElementById('btn-registrar').style.borderColor = "#00f2fe";
            document.getElementById('form-registro').reset();

            cargarJugadores();
        } else {
            mensajeDiv.innerHTML = `<p style="color: red;">❌ Error: ${resultado.error}</p>`;
        }
    } catch (error) {
        console.error("Error en la petición:", error);
        alert("No se pudo conectar con el servidor.");
    }
});

async function cargarJugadores() {
    const contenedor = document.getElementById('contenedor-jugadores');
    if (!contenedor) return;

    try {
        const respuesta = await fetch('http://127.0.0.1:5000/jugadores');
        const jugadores = await respuesta.json();

        contenedor.innerHTML = "";

        jugadores.forEach(jugador => {
            const card = document.createElement('div');
            card.className = 'player-card';
            card.innerHTML = `

                <h3>${jugador.nombre} ${jugador.apellido}</h3>
                <p><strong>⚽ Posición:</strong> ${jugador.posicion}</p>
                <p><strong>🦶 Pie:</strong> ${jugador.pie_dominante}</p>
                <p><strong>📏 Altura:</strong> ${jugador.altura}m | <strong>⚖️ Peso:</strong> ${jugador.peso}kg</p>
                <p>📧 ${jugador.correo}</p>

                <div class="acciones">
                <button class="btn-editar" onclick="prepararEdicion(${jugador.id}, '${jugador.nombre}', '${jugador.apellido}', '${jugador.fecha_nacimiento}', '${jugador.telefono}', '${jugador.correo}', '${jugador.direccion}')">
                Editar
                </button>
                <button class="btn-eliminar" onclick="eliminarJugador(${jugador.id})">
                Eliminar
                </button>
                </div>
            `;
            contenedor.appendChild(card);
        });
    } catch (error) {
        console.error("Error al cargar jugadores:", error);
    }
}
async function eliminarJugador(id) {
    if (confirm("¿Estás seguro de que deseas eliminar a este jugador?")) {
        try {
            const respuesta = await fetch(`http://127.0.0.1:5000/eliminar/${id}`, {
                method: 'DELETE'
            });

            const resultado = await respuesta.json();

            if (respuesta.ok) {
                alert(resultado.mensaje);
                cargarJugadores();
            } else {
                alert("Error: " + resultado.error);
            }
        } catch (error) {
            console.error("Error al eliminar:", error);
            alert("No se pudo conectar con el servidor.");
        }
    }
}

function prepararEdicion(id, nombre, apellido, fecha, tel, correo, dir, pos, pie, alt, peso) {
    document.getElementById('nombre').value = nombre;
    document.getElementById('apellido').value = apellido;
    document.getElementById('fecha_nacimiento').value = fecha;
    document.getElementById('telefono').value = tel;
    document.getElementById('correo').value = correo;
    document.getElementById('direccion').value = dir;
    document.getElementById('posicion').value = pos;
    document.getElementById('pie_dominante').value = pie;
    document.getElementById('altura').value = alt;
    document.getElementById('peso').value = peso;

    editandoId = id;
    document.getElementById('btn-registrar').innerText = "Actualizar Jugador";
    document.getElementById('btn-registrar').style.borderColor = "#ff9f43";
    window.scrollTo(0, 0); 
}
document.addEventListener('DOMContentLoaded', cargarJugadores);