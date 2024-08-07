const { ipcRenderer } = require('electron');

function goHome() {
    ipcRenderer.send('open-page', 'HomeScreen.html');
}
