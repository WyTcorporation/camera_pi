function updateStatus() {
  fetch('/status')
    .then(res => res.json())
    .then(data => {
      let statusText = "";
      for (const [key, value] of Object.entries(data)) {
        const label = key === "audio" ? "🎤 Аудіо" : `📷 ${key.toUpperCase()}`;
        statusText += `${label}: ${value ? "🔴 Запис" : "⏹️ Стоп"}<br>`;
      }
      document.getElementById('status').innerHTML = statusText;
    });
}


function startRecording() {
  fetch('/start').then(updateStatus);
}

function stopRecording() {
  fetch('/stop').then(updateStatus);
}

setInterval(updateStatus, 2000);
