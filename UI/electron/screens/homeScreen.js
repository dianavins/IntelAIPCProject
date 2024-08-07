const { ipcRenderer } = require('electron');

function openPage(page) {
    ipcRenderer.send('open-page', page);
}

function playAudio(type) {
    const audio = new Audio(`path/to/${type}.mp3`);
    audio.play();
}