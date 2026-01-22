const client = mqtt.connect('ws://192.168.0.24:9001');
const registros = [];
const MAX = 500;

let ultimo = {
    temperatura: null,
    luz: null,
    nivel: null,
    estado: null,
    buzzer: null
};

client.on('connect', () => {
    client.subscribe('semillero/#');
});

client.on('message', (topic, message) => {
    const data = JSON.parse(message.toString());

    if (topic.endsWith('temperatura')) ultimo.temperatura = data.value;
    if (topic.endsWith('luz')) ultimo.luz = data.value;
    if (topic.endsWith('nivel')) ultimo.nivel = data.value;
    if (topic.endsWith('sistema')) ultimo.estado = data.estado;
    if (topic.endsWith('buzzer')) ultimo.buzzer = data.buzzer;

    actualizarVista();
});

function actualizarVista() {
    if (ultimo.temperatura !== null &&
        ultimo.luz !== null &&
        ultimo.nivel !== null &&
        ultimo.estado !== null &&
        ultimo.buzzer !== null) {

        document.getElementById('temp').innerText = ultimo.temperatura;
        document.getElementById('luz').innerText = ultimo.luz;
        document.getElementById('nivel').innerText = ultimo.nivel;
        document.getElementById('estado').innerText = ultimo.estado;
        document.getElementById('buzzer').innerText = ultimo.buzzer;

        const registro = {
            hora: new Date().toLocaleTimeString(),
            ...ultimo
        };

        registros.push(registro);
        if (registros.length > MAX) registros.shift();

        renderTabla();
    }
}

function renderTabla() {
    const tbody = document.getElementById('tabla');
    tbody.innerHTML = '';

    registros.forEach(r => {
        const row = `<tr>
      <td>${r.hora}</td>
      <td>${r.temperatura}</td>
      <td>${r.luz}</td>
      <td>${r.nivel}</td>
      <td>${r.estado}</td>
      <td>${r.buzzer}</td>
    </tr>`;
        tbody.innerHTML += row;
    });
}

function apagarBuzzer() {
    client.publish(
        'semillero/control/buzzer',
        JSON.stringify({ command: "OFF" })
    );
}
