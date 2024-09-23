import "../assets/styles/Rack.css";

import { useEffect, useReducer, useState } from "react";

import ToDeviceModule from "./modules/ToDeviceModule";
import OscillatorModule from "./modules/OscillatorModule";
import Cable from "./Cable";

const __TO_DEVICE = 0;
const __FROM_DEVICE = 1;
const __OSCILLATOR = 2;
const __ENVELOPE = 3;
const __FILTER = 4;
const __AMPLIFIER = 5;
const __MIXER = 6;

// function reducer(state, action) {
//   switch (action.type) {
//     case "__MODULE.ADD":
//       break;
//     case "__MODULE.REMOVE":
//       break;
//     case "__MODULE":
//       br
//   }
// }

function Rack() {
  // one key idea --> tie creation and deletion of modules/cables to component lifecycle

  // const [state, dispatch] = useReducer(reducer, {
  //   modules: {},
  //   cables: {},
  //   dragging: { moduleId: null, cableId: null },
  // });

  const [modules, setModules] = useState({ placing: {}, placed: {} });
  const [cables, setCables] = useState({ placing: {}, placed: {} });
  const [dragging, setDragging] = useState({ modules: [], cables: [] });

  // for dragging (Can this be not state?)
  let oldXCoord = 0;
  let oldYCoord = 0;

  // or what if you use mouse coords as state?

  function addModule(moduleType) {
    setModules((modules) => {
      modules = { placing: { ...modules.placing }, placed: { ...modules.placed } };

      let moduleId;
      do {
        moduleId = Math.floor(Math.random() * 1000) + 1;
      } while (moduleId in modules);
      const module = { moduleId, moduleType };

      modules.placed[moduleId] = module; // TODO: placing
      return modules;
    });
  }

  function removeModule(moduleId) {
    setModules((modules) => {
      modules = { placing: { ...modules.placing }, placed: { ...modules.placed } };

      delete modules.placed[moduleId];
      delete modules.placing[moduleId];
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
      cables = { ...cables, placing: { ...cables.placing } };

      let cableId;
      do {
        cableId = Math.floor(Math.random() * 1000) + 1;
      } while (cableId in cables);
      const cable = {
        cableId,
        inModuleId,
        inPortId,
        outModuleId,
        outPortId,
        inXCoord,
        inYCoord,
        outXCoord,
        outYCoord,
      };

      cables.placing[cableId] = cable;
      return cables;
    });
  }

  function updateCable(cableId, args) {}

  function removeCable(cableId) {
    setCables((cables) => {
      cables = { placing: { ...cables.placing }, placed: { ...cables.placed } };

      delete cables.placed[cableId];
      delete cables.placing[cableId];
      return cables;
    });
  }

  function moveCable(xOffset, yOffset) {
    setCables((cables) => {
      cables = { ...cables, placing: { ...cables.placing } };

      for (const cable of Object.values(cables.placing)) {
        if (!cable.inModuleId) {
          cables.placing[cable.cableId] = {
            ...cable,
            inXCoord: cable.inXCoord + xOffset,
            inYCoord: cable.inYCoord + yOffset,
          };
        }
        if (!cable.outModuleId) {
          cables.placing[cable.cableId] = {
            ...cable,
            outXCoord: cable.outXCoord + xOffset,
            outYCoord: cable.outYCoord + yOffset,
          };
        }
      }

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

  // clientX, clientY are relative to viewport while xCoord, yCoord is relative to rack!

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
    if (event.target.classList.contains("port")) {
      const port = event.target;
      const portIcon = port.querySelector(".port-icon");
      let { xCoord, yCoord } = calcRackCoords(portIcon);
      xCoord += portIcon.offsetWidth / 2;
      yCoord += portIcon.offsetHeight / 2;

      if (port.classList.contains("in-port")) {
        addCable(
          parseInt(port.dataset.moduleId),
          parseInt(port.dataset.inPortId),
          null,
          null,
          xCoord,
          yCoord,
          event.clientX,
          event.clientY
        );
      }
      if (port.classList.contains("out-port")) {
        addCable(
          null,
          null,
          parseInt(port.dataset.moduleId),
          parseInt(port.dataset.outPortId),
          event.clientX,
          event.clientY,
          xCoord,
          yCoord
        );
      }

      oldXCoord = event.clientX;
      oldYCoord = event.clientY;

      const rack = port.closest(".rack-inner");
      rack.onmousemove = handleMouseMove;
      rack.onmouseup = handleMouseUp;

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

    moveCable(xOffset, yOffset);
  }

  function handleMouseUp(event) {
    let port = null;

    const elements = document.elementsFromPoint(event.clientX, event.clientY);
    for (const element of elements) {
      if (element.classList.contains("port")) {
        port = element;
        break;
      }
    }

    if (port) {
      const portIcon = port.querySelector(".port-icon");
      let { xCoord, yCoord } = calcRackCoords(portIcon);
      xCoord += portIcon.offsetWidth / 2;
      yCoord += portIcon.offsetHeight / 2;

      setCables((cables) => {
        cables = { placing: { ...cables.placing }, placed: { ...cables.placed } };

        for (const cable of Object.values(cables.placing)) {
          if (!cable.inModuleId && port.classList.contains("in-port")) {
            cables.placed[cable.cableId] = {
              ...cable,
              inModuleId: parseInt(port.dataset.moduleId),
              inPortId: parseInt(port.dataset.inPortId),
              inXCoord: xCoord,
              inYCoord: yCoord,
            };
          }
          if (!cable.outModuleId && port.classList.contains("out-port")) {
            cables.placed[cable.cableId] = {
              ...cable,
              outModuleId: parseInt(port.dataset.moduleId),
              outPortId: parseInt(port.dataset.outPortId),
              outXCoord: xCoord,
              outYCoord: yCoord,
            };
          }
        }

        // actually, this has to happen anyway, so either the DOM stuff is put inside here or this line is a separate call
        cables.placing = {};

        console.log(cables);

        return cables;
      });

      const rack = event.target.closest(".rack-inner");
      rack.onmousemove = null;
      rack.onmouseup = null;

      return;
    }

    setCables((cables) => {
      cables = { ...cables, placing: {} };
      return cables;
    });
  }

  return (
    <div className="rack-outer">
      <div className="rack-inner" onMouseDown={handleMouseDown}>
        {[...Object.values(modules.placing), ...Object.values(modules.placed)].map((module, i) => {
          const props = {
            moduleId: module.moduleId,
            xCoord: 200 * i,
            yCoord: 200,
          };

          switch (module.moduleType) {
            case __TO_DEVICE:
              return <ToDeviceModule key={module.moduleId} {...props} />;
            case __FROM_DEVICE:
              return;
            case __OSCILLATOR:
              return <OscillatorModule key={module.moduleId} {...props} />;
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
        {[...Object.values(cables.placing), ...Object.values(cables.placed)].map((cable) => {
          const props = {
            cableId: cable.cableId,
            inModuleId: cable.inModuleId,
            inPortId: cable.inPortId,
            outModuleId: cable.outModuleId,
            outPortId: cable.outPortId,
            inXCoord: cable.inXCoord,
            inYCoord: cable.inYCoord,
            outXCoord: cable.outXCoord,
            outYCoord: cable.outYCoord,
          };

          return <Cable key={cable.cableId} {...props} />;
        })}
        {/* <div
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
        </div> */}
      </div>
      <div className="rack-widget">
        <button onClick={() => addModule(__TO_DEVICE)}>TO DEVICE</button>
        <button onClick={() => addModule(__OSCILLATOR)}>VCO</button>
      </div>
    </div>
  );
}

export default Rack;
