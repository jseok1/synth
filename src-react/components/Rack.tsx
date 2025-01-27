import "../assets/styles/Rack.css";

import { ReactElement, useEffect, useRef, useState } from "react";
import { v4 as uuid } from "uuid";

import ToDeviceModule, { ToDeviceInPort, ToDeviceOutPort } from "./modules/ToDeviceModule";
import OscillatorModule, {
  OscillatorInPorts,
  OscillatorOutPorts,
  OscillatorWidth,
  OscillatorHeight,
} from "./modules/OscillatorModule";
import FilterModule, { FilterInPort, FilterOutPort } from "./modules/FilterModule";
import Cable from "./Cable";

enum ModuleType {
  __TO_DEVICE,
  __FROM_DEVICE,
  __OSCILLATOR,
  __ENVELOPE,
  __FILTER,
  __AMPLIFIER,
  __MIXER,
}

interface Module {
  moduleId: string;
  inPorts: {
    [inPortType: number]: { cableId: string };
  };
  outPorts: {
    [outPortType: number]: { cableIds: string[] };
  };
  xCoord: number;
  yCoord: number;
  isDraggable: boolean;
  width: number;
  height: number;
}

interface Cable {
  cableId: string;
  inModuleId: string;
  inPortType: number;
  outModuleId: string;
  outPortType: number;
  inXCoord: number;
  inYCoord: number;
  outXCoord: number;
  outYCoord: number;
  zCoord: number;
  inIsDraggable: boolean;
  outIsDraggable: boolean;
}

// say only 1 thing can be selected at a time: selected: { id: moving type: "module" | "cable-in" | "cable-out" }

interface Rack {
  modules: {
    [moduleId: string]: Module;
  };
  cables: {
    [cableId: string]: Cable;
  };
}

// in pixels
const UNIT_X = 50;
const UNIT_Y = 50 * 8;

function Rack(): ReactElement<any, any> | null {
  const [{ modules, cables }, setRack] = useState<Rack>({ modules: {}, cables: {} });

  const rackElement = useRef<HTMLDivElement>(null);
  const cursorCoords = useRef<{ xCoord: number; yCoord: number }>({ xCoord: 0, yCoord: 0 });

  function calcCoords(element: HTMLElement): { xCoord: number; yCoord: number } {
    let xCoord = 0;
    let yCoord = 0;
    while (element && element !== rackElement.current) {
      // TODO: padding, margin, border, outline
      // includes padding but not border
      const { borderLeftWidth, borderTopWidth } = getComputedStyle(element);
      xCoord += element.offsetLeft + parseFloat(borderLeftWidth);
      yCoord += element.offsetTop + parseFloat(borderTopWidth);
      element = element.offsetParent as HTMLElement;
    }

    return { xCoord, yCoord };
  }

  function addModule({ modules, cables }: Rack, moduleType: ModuleType): Rack {
    modules = { ...modules };

    let moduleId: string;
    do {
      moduleId = uuid();
    } while (moduleId in modules);

    modules[moduleId] = {
      moduleId,
      inPorts: {},
      outPorts: {},
      xCoord: 0,
      yCoord: 0,
      isDraggable: false,
      width: 0,
      height: 0,
    };

    let inPorts: number[];
    let outPorts: number[];
    let width: number;
    let height: number;
    switch (moduleType) {
      case ModuleType.__TO_DEVICE:
        inPorts = ToDeviceInPort;
        outPorts = ToDeviceOutPort;
        width = OscillatorWidth;
        height = OscillatorHeight;
        break;
      case ModuleType.__FROM_DEVICE:
        inPorts = FilterInPort;
        outPorts = FilterOutPort;
        width = OscillatorWidth;
        height = OscillatorHeight;
        break;
      case ModuleType.__OSCILLATOR:
        inPorts = OscillatorInPorts;
        outPorts = OscillatorOutPorts;
        width = OscillatorWidth;
        height = OscillatorHeight;
        break;
      case ModuleType.__ENVELOPE:
        inPorts = FilterInPort;
        outPorts = FilterOutPort;
        width = OscillatorWidth;
        height = OscillatorHeight;
        break;
      case ModuleType.__FILTER:
        inPorts = FilterInPort;
        outPorts = FilterOutPort;
        width = OscillatorWidth;
        height = OscillatorHeight;
        break;
      case ModuleType.__AMPLIFIER:
        inPorts = FilterInPort;
        outPorts = FilterOutPort;
        width = OscillatorWidth;
        height = OscillatorHeight;
        break;
      case ModuleType.__MIXER:
        inPorts = FilterInPort;
        outPorts = FilterOutPort;
        width = OscillatorWidth;
        height = OscillatorHeight;
        break;
      default:
        throw new Error("RACK::moduleType is invalid");
    }

    for (const inPort of inPorts) {
      modules[moduleId].inPorts[inPort] = { cableId: "" };
    }

    for (const outPort of outPorts) {
      modules[moduleId].outPorts[outPort] = { cableIds: [] };
    }

    modules[moduleId].width = width;
    modules[moduleId].height = height;

    return { modules, cables };
  }

  function removeModule({ modules, cables }: Rack, moduleId: string): Rack {
    modules = { ...modules };
    cables = { ...cables };

    for (const inPort of Object.values(modules[moduleId].inPorts)) {
      ({ modules, cables } = removeCable({ modules, cables }, inPort.cableId));
    }

    for (const outPort of Object.values(modules[moduleId].outPorts)) {
      for (const cableId of outPort.cableIds) {
        ({ modules, cables } = removeCable({ modules, cables }, cableId));
      }
    }

    delete modules[moduleId];

    return { modules, cables };
  }

  function dragModule(
    { modules, cables }: Rack,
    moduleId: string,
    xOffset: number,
    yOffset: number
  ): Rack {
    modules = { ...modules };

    modules[moduleId] = {
      ...modules[moduleId],
      xCoord: modules[moduleId].xCoord + xOffset,
      yCoord: modules[moduleId].yCoord + yOffset,
    };

    for (const inPort of Object.values(modules[moduleId].inPorts)) {
      ({ modules, cables } = dragCable({ modules, cables }, inPort.cableId, xOffset, yOffset));
    }

    for (const outPort of Object.values(modules[moduleId].outPorts)) {
      for (const cableId of outPort.cableIds) {
        ({ modules, cables } = dragCable({ modules, cables }, cableId, xOffset, yOffset));
      }
    }

    return { modules, cables };
  }

  function addCable(
    { modules, cables }: Rack,
    inModuleId: string,
    inPortType: number,
    outModuleId: string,
    outPortType: number,
    inXCoord: number,
    inYCoord: number,
    outXCoord: number,
    outYCoord: number,
    zCoord: number
  ): Rack {
    cables = { ...cables };

    let cableId: string;
    do {
      cableId = uuid();
    } while (cableId in cables);
    cables[cableId] = {
      cableId,
      inModuleId,
      inPortType,
      outModuleId,
      outPortType,
      inXCoord,
      inYCoord,
      outXCoord,
      outYCoord,
      zCoord,
      inIsDraggable: false,
      outIsDraggable: false,
    };

    return { modules, cables };
  }

  function removeCable({ modules, cables }: Rack, cableId: string): Rack {
    cables = { ...cables };

    const cable = cables[cableId];

    if (cable.inModuleId && cable.inPortType) {
      const inPort = modules[cable.inModuleId].inPorts[cable.inPortType];
      inPort.cableId = "";
    }

    if (cable.outModuleId && cable.outPortType) {
      const outPort = modules[cable.outModuleId].outPorts[cable.outPortType];
      outPort.cableIds = outPort.cableIds.filter(
        (cableId: string): boolean => cableId !== cable.cableId // cable.cableId
      );
    }

    delete cables[cableId];

    return { modules, cables };
  }

  function dragCable(
    { modules, cables }: Rack,
    cableId: string,
    inXOffset: number,
    inYOffset: number,
    outXOffset: number,
    outYOffset: number
  ): Rack {
    cables = { ...cables };

    cables[cableId] = {
      ...cables[cableId],
      inXCoord: cables[cableId].inXCoord + inXOffset,
      inYCoord: cables[cableId].inYCoord + inYOffset,
      outXCoord: cables[cableId].outXCoord + outXOffset,
      outYCoord: cables[cableId].outYCoord + outYOffset,
    };

    return { modules, cables };
  }

  // TODO: this is a hack
  const timeoutId = useRef<NodeJS.Timeout | null>(null);
  useEffect(() => {
    if (!timeoutId.current) {
      timeoutId.current = setTimeout(function () {
        console.log("api.startStream();");
        window.api.engine.startStream();
        timeoutId.current = null;
      }, 1000);
    }
    return () => {
      if (!timeoutId.current) {
        console.log("api.stopStream();");
        window.api.engine.stopStream();
      }
    };
  }, []);

  function handleMouseDown(event: MouseEvent): void {
    cursorCoords.current.xCoord = event.clientX;
    cursorCoords.current.yCoord = event.clientY;
  }

  function handleMouseMove(event: MouseEvent): void {
    const xOffset = event.clientX - cursorCoords.current.xCoord;
    const yOffset = event.clientY - cursorCoords.current.yCoord;

    cursorCoords.current.xCoord = event.clientX;
    cursorCoords.current.yCoord = event.clientY;

    setRack(({ modules, cables }: Rack): Rack => {
      modules = { ...modules };
      cables = { ...cables };

      for (const [moduleId, module] of Object.entries(modules)) {
        if (module.isDraggable) {
          ({ modules, cables } = dragModule({ modules, cables }, moduleId, xOffset, yOffset));
        }
      }

      for (const [cableId, cable] of Object.entries(cables)) {
        if (cable.inIsDraggable) {
          cables[cableId] = {
            ...cable,
            inXCoord: cable.inXCoord + xOffset,
            inYCoord: cable.inYCoord + yOffset,
          };
        }

        if (cable.outIsDraggable) {
          cables[cableId] = {
            ...cable,
            outXCoord: cable.outXCoord + xOffset,
            outYCoord: cable.outYCoord + yOffset,
          };
        }
      }

      return { modules, cables };
    });
  }

  function handleMouseUp(event: MouseEvent): void {
    setRack(({ modules, cables }: Rack): Rack => {
      modules = { ...modules };
      cables = { ...cables };

      for (const [moduleId, module] of Object.entries(modules)) {
        if (module.isDraggable) {
          const xOffset = Math.max(0, Math.round(module.xCoord / UNIT_X) * UNIT_X) - module.xCoord;
          const yOffset = Math.max(0, Math.round(module.yCoord / UNIT_Y) * UNIT_Y) - module.yCoord;

          ({ modules, cables } = dragModule({ modules, cables }, moduleId, xOffset, yOffset));
        }
      }

      const yCoords: { [yCoord: number]: string[] } = {};
      for (const module of Object.values(modules)) {
        if (!yCoords[module.yCoord]) {
          yCoords[module.yCoord] = [];
        }
        yCoords[module.yCoord].push(module.moduleId);
      }

      for (const moduleIds of Object.values(yCoords)) {
        moduleIds.sort(
          (thisModuleId, thatModuleId) =>
            modules[thisModuleId].xCoord - modules[thatModuleId].xCoord
        );

        let xOffset = 0;
        for (const moduleId of moduleIds) {
          ({ modules, cables } = dragModule({ modules, cables }, moduleId, xOffset, 0));
          xOffset += modules[moduleId].width;
        }
      }

      for (const [cableId, cable] of Object.entries(cables)) {
        if (cable.inIsDraggable) {
          delete cables[cableId];
        }

        if (cable.outIsDraggable) {
          delete cables[cableId];
        }
      }

      return { modules, cables };
    });
  }

  // mouseDown --> isDraggable = true for cables/modules
  // mouseMove --> isDraggable cables/modules
  // mouseUp --> isDraggable = false for cables/modules AND snap
  // need to apply snap offset to cables

  // useeffect -> check all isdragging modules, then set cable whose in/out port is that module

  // maybe dragModule isn't necessary

  return (
    <div className="rack-outer">
      <div
        className="rack-inner"
        ref={rackElement}
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
      >
        {Object.values(modules).map((module, i) => {
          switch (module.moduleType) {
            case ModuleType.__TO_DEVICE:
              return (
                <ToDeviceModule
                  key={module.moduleId}
                  {...module}
                  setRack={setRack}
                  calcCoords={calcCoords}
                />
              );
            case ModuleType.__FROM_DEVICE:
              return;
            case ModuleType.__OSCILLATOR:
              return (
                <OscillatorModule
                  key={module.moduleId}
                  {...module}
                  setRack={setRack}
                  calcCoords={calcCoords}
                />
              );
            case ModuleType.__ENVELOPE:
              return;
            case ModuleType.__FILTER:
              return (
                <FilterModule
                  key={module.moduleId}
                  {...module}
                  setRack={setRack}
                  calcCoords={calcCoords}
                />
              );
            case ModuleType.__AMPLIFIER:
              return;
            case ModuleType.__MIXER:
              return;
            default:
              throw new Error("RACK::moduleType is invalid");
          }
        })}
        {Object.values(cables).map((cable) => (
          <Cable key={cable.cableId} {...cable} />
        ))}
      </div>
      <div className="rack-widget">
        <button
          onClick={() => {
            setRack(({ modules, cables }) =>
              addModule({ modules, cables }, ModuleType.__TO_DEVICE)
            );
          }}
        >
          TO DEVICE
        </button>
        <button
          onClick={() => {
            setRack(({ modules, cables }) =>
              addModule({ modules, cables }, ModuleType.__OSCILLATOR)
            );
          }}
        >
          VCO
        </button>
        <button
          onClick={() => {
            setRack(({ modules, cables }) => addModule({ modules, cables }, ModuleType.__FILTER));
          }}
        >
          VCF
        </button>
      </div>
    </div>
  );
}

export default Rack;
