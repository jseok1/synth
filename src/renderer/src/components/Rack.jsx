import "../assets/styles/Rack.css";

import { useEffect, useState } from "react";

import ToDeviceModule from "./ToDeviceModule";
import OscillatorModule from "./OscillatorModule";
import Cable from "./Cable";

const __TO_DEVICE = 0;
const __FROM_DEVICE = 1;
const __OSCILLATOR = 2;
const __ENVELOPE = 3;
const __FILTER = 4;
const __AMPLIFIER = 5;
const __MIXER = 6;

function Rack() {
  // one key idea --> tie creation and deletion of modules/cables to component lifecycle

  const [modules, setModules] = useState({});
  const [cables, setCables] = useState({});
  // let draggingModuleId = null;
  let activeCable = {}; // synchronous version of state (in module + port identify cable, must also identify which head is being moved)

  // for dragging
  let oldXCoord = 0;
  let oldYCoord = 0;

  function addModule(moduleType) {
    setModules((modules) => {
      let moduleId;
      do {
        moduleId = Math.floor(Math.random() * 1000) + 1;
      } while (moduleId in modules);

      const module = { moduleId, moduleType };
      modules = { ...modules };
      modules[moduleId] = module;

      return modules;
    });
  }

  function removeModule(moduleId) {
    setModules((modules) => {
      modules = { ...modules };
      delete modules[moduleId];

      return modules;
    });
  }

  function addCable(
    inModuleId,
    inPortId,
    outModuleId,
    outPortId,
    inXCoord,
    inYCoord,
    outXCoord,
    outYCoord
  ) {
    setCables((cables) => {
      const cable = {
        inModuleId,
        inPortId,
        outModuleId,
        outPortId,
        inXCoord,
        inYCoord,
        outXCoord,
        outYCoord,
      };

      cables = { ...cables };
      if (!cables[inModuleId]) cables[inModuleId] = {};
      cables[inModuleId][inPortId] = cable;

      return cables;
    });
  }

  function updateCable(inModuleId, inPortId, args) {
    setCables((cables) => {
      const cable = { ...cables[inModuleId][inPortId], ...args };
      cables = { ...cables };
      cables[inModuleId][inPortId] = cable;

      return cables;
    });
  }

  useEffect(() => {
    // api.addCable(0, 0, 1, 1);
    // console.log("api.startStream();");
    // api.startStream();
    return () => {
      // console.log("api.stopStream();");
      // api.stopStream();
    };
  }, []);

  // CABLES =====

  function calcRackCoords(element) {
    let xCoord = 0;
    let yCoord = 0;

    while (!element.classList.contains("rack-inner")) {
      // TODO: padding, margin, border, outline
      // includes padding but not border
      const { borderLeftWidth, borderTopWidth } = getComputedStyle(element);
      xCoord += parseFloat(element.offsetLeft) + parseFloat(borderLeftWidth.slice(0, -2));
      yCoord += parseFloat(element.offsetTop) + parseFloat(borderTopWidth.slice(0, -2));
      element = element.offsetParent;
    }

    return { xCoord, yCoord };
  }

  function handleMouseDown(event) {
    console.log(event.target);
    if (event.target.classList.contains("in-port")) {
      // inport vs. outport
      const inPort = event.target;
      // and does not have cable already...
      // not the most "React" way...
      let { xCoord, yCoord } = calcRackCoords(inPort.querySelector(".port-icon"));
      xCoord += inPort.querySelector(".port-icon").offsetWidth / 2;
      yCoord += inPort.querySelector(".port-icon").offsetHeight / 2;

      const rack = inPort.closest(".rack-inner");

      // TODO: think about whether data-module-id or data-in-module-id makes more sense
      let { moduleId: inModuleId, inPortId } = inPort.dataset;
      inModuleId = parseInt(inModuleId);
      inPortId = parseInt(inPortId);
      // clientX, clientY are relative to viewport while xCoord, yCoord is relative to rack!
      addCable(inModuleId, inPortId, null, null, xCoord, yCoord, event.clientX, event.clientY);
      activeCable = {
        inModuleId,
        inPortId,
        inXCoord: xCoord,
        inYCoord: yCoord,
        outXCoord: event.clientX,
        outYCoord: event.clientY,
      };

      // actually maybe it's fine to set via state since you're still recording the old coords here
      rack.onmousemove = handleMouseMove;
      rack.onmouseup = handleMouseUp;

      oldXCoord = event.clientX;
      oldYCoord = event.clientY;

      return;
    }

    if (event.target.classList.contains("module")) {
      return;
    }
  }

  function handleMouseMove(event) {
    const newXCoord = event.clientX;
    const newYCoord = event.clientY;

    const xOffset = newXCoord - oldXCoord;
    const yOffset = newYCoord - oldYCoord;

    oldXCoord = newXCoord;
    oldYCoord = newYCoord;

    const { inModuleId, inPortId } = activeCable;
    // updateCable(inModuleId, inPortId, outXCoord, outYCoord);
    activeCable.outXCoord += xOffset;
    activeCable.outYCoord += yOffset;

    setCables((cables) => {
      const cable = {
        ...cables[inModuleId][inPortId],
        outXCoord: activeCable.outXCoord,
        outYCoord: activeCable.outYCoord,
      };
      cables = { ...cables };
      cables[inModuleId][inPortId] = cable;

      return cables;
    });

    // if the mouse goes outside the window, cancel
    // dragging might break when scrolling simultaneously since clientX/Y are relative to viewport
  }

  function handleMouseUp(event) {
    const maybe = document.elementsFromPoint(event.clientX, event.clientY);
    let inPort = null;
    for (const element of maybe) {
      if (element.classList.contains("in-port")) {
        inPort = element;
        break;
      }
    }
    if (inPort) {
      // and does not have cable already...
      let { xCoord: outXCoord, yCoord: outYCoord } = calcRackCoords(
        inPort.querySelector(".port-icon")
      );
      outXCoord += inPort.querySelector(".port-icon").offsetWidth / 2;
      outYCoord += inPort.querySelector(".port-icon").offsetHeight / 2;

      const { inModuleId, inPortId } = activeCable;
      let { moduleId: outModuleId, inPortId: outPortId } = inPort.dataset; // TODO: outport
      outModuleId = parseInt(outModuleId);
      outPortId = parseInt(outPortId);
      console.log(inModuleId, inPortId, outModuleId, outPortId);
      updateCable(inModuleId, inPortId, { outModuleId, outPortId, outXCoord, outYCoord });

      const rack = event.target.closest(".rack-inner");
      rack.onmousemove = null;
      rack.onmouseup = null;

      return;
    } else {
      // setCables([]);
    }

    // else cancel
  }

  // CABLES =====

  return (
    <div className="rack-outer">
      <div className="rack-inner" onMouseDown={handleMouseDown}>
        {Object.values(modules).map((module, i) => {
          const { moduleId, moduleType } = module;
          const props = {
            moduleId: moduleId,
            xCoord: 200 * i,
            yCoord: 200,
          };

          switch (moduleType) {
            case __TO_DEVICE:
              return <ToDeviceModule key={moduleId} {...props} />;
            case __FROM_DEVICE:
              return;
            case __OSCILLATOR:
              return <OscillatorModule key={moduleId} {...props} />;
            case __ENVELOPE:
              return;
            case __FILTER:
              return;
            case __AMPLIFIER:
              return;
            case __MIXER:
              return;
            default:
              throw new Error("RACK::moduleType is invalid");
          }
        })}
        {Object.values(cables)
          .map((cables) =>
            Object.values(cables).map((cable) => {
              const {
                inModuleId,
                inPortId,
                outModuleId,
                outPortId,
                inXCoord,
                inYCoord,
                outXCoord,
                outYCoord,
              } = cable;
              const props = {
                inModuleId,
                inPortId,
                outModuleId,
                outPortId,
                inXCoord,
                inYCoord,
                outXCoord,
                outYCoord,
              };

              return <Cable key={inModuleId + " " + inPortId} {...props} />;
            })
          )
          .flat()}
        <div
          id="red-point"
          style={{
            position: "absolute",
            width: "1px",
            height: "1px",
            overflow: "visible",
            backgroundColor: "red",
          }}
        >
          <div
            style={{
              width: "15px",
              height: "15px",
              border: "2px solid red",
              borderRadius: "50%",
              position: "absolute",
              transform: "translate(-50%, -50%)",
            }}
          ></div>
        </div>
      </div>
      <div className="rack-widget">
        <button onClick={() => addModule(__TO_DEVICE)}>TO DEVICE</button>
        <button onClick={() => addModule(__OSCILLATOR)}>VCO</button>
      </div>
    </div>
  );
}

export default Rack;
