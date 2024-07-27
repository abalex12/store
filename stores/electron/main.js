const { app, BrowserWindow } = require('electron');
const path = require('path');

function createWindow () {
  const win = new BrowserWindow({
    width: 1920,
    height: 720,
    fullscreenable: true,  // Allow the window to enter and exit fullscreen mode
    autoHideMenuBar: true,  // Hide menu bar in fullscreen mode
    resizable: true, 
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
    }
  });

  win.loadURL('http://localhost:8000');  
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
