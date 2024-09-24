const { app, BrowserWindow, ipcMain } = require('electron');
const axios = require('axios');
const path = require('path');

let mainWindow;

function createWindow() {
    const mainWindow = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            // preload: path.join(__dirname, 'preload.js'),
            contextIsolation: false,
            nodeIntegration: true,
        },
    });

    mainWindow.setMenu(null);

    mainWindow.loadFile(path.join(__dirname, 'screens', 'HomeScreen.html'));

    ipcMain.on('open-page', (event, page) => {
        mainWindow.loadFile(path.join(__dirname, 'screens', page));
    });
    mainWindow.webContents.openDevTools();
}

app.on('ready', createWindow);

// function createStoryTellerWindow() {
//     const storyTellerWindow = new BrowserWindow({
//         webPreferences: {
//             contextIsolation: true,
//             nodeIntegration: false
//         }
//     });
//     storyTellerWindow.loadFile('screens/storyTeller.html');
//     return storyTellerWindow;
// }

ipcMain.on('generate-story-request', () => {
    console.log("Received IPC message for story generation");
    axios.get('http://localhost:5000/generate_story_and_images')
        .then(response => {
            // Assuming createStoryTellerWindow and the window communication is correct
            const storyTellerWindow = createStoryTellerWindow();
            storyTellerWindow.webContents.once('did-finish-load', () => {
                storyTellerWindow.webContents.send('story-update', {
                    story: response.data.story,
                    images: response.data.images
                });
            });
        })
        .catch(error => {
            console.error('Failed to fetch data:', error);
        });
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});