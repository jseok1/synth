import "../assets/styles/Rack.css";

import { useEffect, useRef, useState } from "react";

import ToDeviceModule from "./modules/ToDeviceModule";
import OscillatorModule from "./modules/OscillatorModule";
import FilterModule from "./modules/FilterModule";
import Cable from "./Cable";

const __TO_DEVICE = 0;
const __FROM_DEVICE = 1;
const __OSCILLATOR = 2;
const __ENVELOPE = 3;
const __FILTER = 4;
const __AMPLIFIER = 5;
const __MIXER = 6;

function Rack() {
  const [modules, setModules] = useState({});
  const [cables, setCables] = useState({});
  const rackElement = useRef(null);
  const cursorCoords = useRef({ xCoord: 0, yCoord: 0 });

  function calcCoords(element) {
    let xCoord = 0;
    let yCoord = 0;

    while (element !== rackElement.current) {
      // TODO: padding, margin, border, outline
      // includes padding but not border
      const { borderLeftWidth, borderTopWidth } = getComputedStyle(element);
      xCoord += parseFloat(element.offsetLeft) + parseFloat(borderLeftWidth);
      yCoord += parseFloat(element.offsetTop) + parseFloat(borderTopWidth);
      element = element.offsetParent;
    }

    return { xCoord, yCoord };
  }

  function addModule(moduleType) {
    setModules((modules) => {
      modules = { ...modules };

      let moduleId;
      do {
        moduleId = Math.floor(Math.random() * 1000) + 1;
      } while (moduleId in modules);
      const module = { moduleId, moduleType, xCoord: 0, yCoord: 0, isDragging: false };

      modules[moduleId] = module;
      return modules;
    });
  }

  // TODO: this is a hack
  const timeoutId = useRef(null);
  useEffect(() => {
    if (!timeoutId.current) {
      timeoutId.current = setTimeout(function () {
        console.log("api.startStream();");
        api.startStream();
        timeoutId.current = null;
      }, 1000);
    }
    return () => {
      if (!timeoutId.current) {
        console.log("api.stopStream();");
        api.stopStream();
      }
    };
  }, []);

  function handleMouseDown(event) {
    cursorCoords.current.xCoord = event.clientX;
    cursorCoords.current.yCoord = event.clientY;
  }

  function handleMouseMove(event) {
    const xOffset = event.clientX - cursorCoords.current.xCoord;
    const yOffset = event.clientY - cursorCoords.current.yCoord;

    cursorCoords.current.xCoord = event.clientX;
    cursorCoords.current.yCoord = event.clientY;

    setModules((modules) => {
      modules = { ...modules };

      for (const [moduleId, module] of Object.entries(modules)) {
        if (module.isDragging) {
          modules[moduleId] = {
            ...module,
            xCoord: module.xCoord + xOffset,
            yCoord: module.yCoord + yOffset,
          };
        }
      }

      return modules;
    });

    setCables((cables) => {
      cables = { ...cables };

      for (const [cableId, cable] of Object.entries(cables)) {
        if (cable.inIsDragging) {
          cables[cableId] = {
            ...cable,
            inXCoord: cable.inXCoord + xOffset,
            inYCoord: cable.inYCoord + yOffset,
          };
        }
        if (cable.outIsDragging) {
          cables[cableId] = {
            ...cable,
            outXCoord: cable.outXCoord + xOffset,
            outYCoord: cable.outYCoord + yOffset,
          };
        }
      }

      return cables;
    });
  }

  function handleMouseUp(event) {
    setModules((modules) => {
      modules = { ...modules };

      for (const [moduleId, module] of Object.entries(modules)) {
        if (module.isDragging) {
          modules[moduleId] = { ...module, isDragging: false };
        }
      }

      return modules;
    });

    setCables((cables) => {
      cables = { ...cables };

      for (const [cableId, cable] of Object.entries(cables)) {
        if (cable.inIsDragging) {
          // TODO: !== null necessary because of 0 falsy for port IDs
          if (cable.inModuleId !== null && cable.inPortId !== null) {
            cables[cableId] = { ...cable, inIsDragging: false };
          } else {
            delete cables[cableId];
          }
        }

        if (cable.outIsDragging) {
          if (cable.outModuleId !== null && cable.outPortId !== null) {
            cables[cableId] = { ...cable, outIsDragging: false };
          } else {
            delete cables[cableId];
          }
        }
      }

      return cables;
    });
  }

  /**
   * setCables and setModules are props
   *
   * mouseDown (rack and inport and outport) -> setCable is moving and create if not there
   * event.stopPropogation()
   * mouseMove (rack) -> update cable pos of all is moving
   * mouseUp (rack and inport and outport) -> for all is moving, check if position is droppable and if so snap to pos
   */

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
            case __TO_DEVICE:
              return (
                <ToDeviceModule
                  key={module.moduleId}
                  {...module}
                  setModules={setModules}
                  setCables={setCables}
                  calcCoords={calcCoords}
                />
              );
            case __FROM_DEVICE:
              return;
            case __OSCILLATOR:
              return (
                <OscillatorModule
                  key={module.moduleId}
                  {...module}
                  setModules={setModules}
                  setCables={setCables}
                  calcCoords={calcCoords}
                />
              );
            case __ENVELOPE:
              return;
            case __FILTER:
              return (
                <FilterModule
                  key={module.moduleId}
                  {...module}
                  setModules={setModules}
                  setCables={setCables}
                  calcCoords={calcCoords}
                />
              );
            case __AMPLIFIER:
              return;
            case __MIXER:
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
        <button onClick={() => addModule(__TO_DEVICE)}>TO DEVICE</button>
        <button onClick={() => addModule(__OSCILLATOR)}>VCO</button>
        <button onClick={() => addModule(__FILTER)}>VCF</button>
      </div>
    </div>
  );
}

export default Rack;
