import { ElectronAPI } from "@electron-toolkit/preload";

declare global {
  interface Window {
    electron: ElectronAPI;
    api: {
      engine: {
        startStream: () => void;
        stopStream: () => void;
        addModule: (moduleId: number, moduleType: number) => void;
        removeModule: (moduleId: number) => void;
        updateParam: (moduleId: number, paramId: number, param: number) => void;
        addCable: (
          inModuleId: number,
          inPortType: number,
          outModuleId: number,
          outPortType: number
        ) => void;
        removeCable: (inModuleId: number, inPortType: number) => void;
      };
    };
  }
}
