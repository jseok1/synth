import { contextBridge } from "electron";
import { electronAPI } from "@electron-toolkit/preload";

import core from "../../resources/core.node";

// Custom APIs for renderer
const api = {
  hello: core.hello,
  startStream: core.startStream,
  stopStream: core.stopStream,
  addModule: core.addModule,
  removeModule: core.removeModule,
  updateParam: core.updateParam,
  addCable: core.addCable,
  removeCable: core.removeCable,
};

// Use `contextBridge` APIs to expose Electron APIs to
// renderer only if context isolation is enabled, otherwise
// just add to the DOM global.
if (process.contextIsolated) {
  try {
    contextBridge.exposeInMainWorld("electron", electronAPI);
    contextBridge.exposeInMainWorld("api", api);
  } catch (error) {
    console.error(error);
  }
} else {
  window.electron = electronAPI;
  window.api = api;
}
