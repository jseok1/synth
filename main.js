const { app, BrowserWindow } = require("electron");
const path = require("node:path");

const core = require("./build/Release/core.node");
core.startStream();
core.addModule(0, 0);
core.addModule(1, 0);
core.addModule(2, 0);
core.addModule(3, 0);
core.addCable(0, 0, 1, 0);
core.addCable(0, 1, 2, 0);
core.addCable(3, 0, 0, 0);
setTimeout(() => {
  core.stopStream();
}, 3000);
// state = {
//   a: 0,
//   b: 0,
//   c: 0,
//   d: 0,
//   e: 0,
// };
// core.runCallback(function () {
//   // console.log(msg); // 'hello world'
//   // console.log(msg); // 'hello world'
//   let count = 0;
//   for (let i = 0; i < 1000; i++) {
//     count += i;
//   }
//   return null;
// });

const createWindow = () => {
  const win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, "preload.js"),
      nodeIntegration: true,
      contextIsolation: false,
    },
  });

  win.loadFile("index.html");
};

app.whenReady().then(() => {
  createWindow();

  app.on("activate", () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    app.quit();
  }
});
