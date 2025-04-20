function updateStatus() {
  fetch('/status')
    .then(res => res.json())
    .then(data => {
      document.getElementById('status').innerText = "Статус: " + (data.recording ? "🔴 Запис" : "⏹️ Зупинено");
    });
}

function startRecording() {
  fetch('/start').then(updateStatus);
}

function stopRecording() {
  fetch('/stop').then(updateStatus);
}

setInterval(updateStatus, 2000);
