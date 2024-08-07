const { ipcRenderer } = require('electron');

function goHome() {
    ipcRenderer.send('open-page', 'HomeScreen.html');
}

function goToStoryTelling() {
    ipcRenderer.send('open-page', 'storyTeller.html');
}
