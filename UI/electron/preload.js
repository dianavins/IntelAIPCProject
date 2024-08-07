const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('api', {
  openScreen: (screenName) => ipcRenderer.send('open-screen', screenName),
});
