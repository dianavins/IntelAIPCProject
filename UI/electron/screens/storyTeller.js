const { ipcRenderer } = require('electron');

function goHome() {
    ipcRenderer.send('open-page', 'HomeScreen.html');
}

function goLeft() {
    // Add your logic for the left arrow button click
    console.log('Left arrow clicked');
}

function goRight() {
    // Add your logic for the right arrow button click
    console.log('Right arrow clicked');
}
