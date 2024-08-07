const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');

function createWindow() {
    const mainWindow = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            preload: path.join(__dirname, 'screens', 'HomeScreen.js'),
            contextIsolation: false,
            nodeIntegration: true,
        },
    });

    mainWindow.setMenu(null);

    mainWindow.loadFile(path.join(__dirname, 'screens', 'HomeScreen.html'));

    ipcMain.on('open-page', (event, page) => {
        mainWindow.loadFile(path.join(__dirname, 'screens', page));
    });
}

app.on('ready', createWindow);

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow();
    }
});
