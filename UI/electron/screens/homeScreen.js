const { ipcRenderer } = require('electron');

function openPage(page) {
    ipcRenderer.send('open-page', page);
}
