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
  let count = 0;
  const [modules, setModules] = useState([]);
  const [cables, setCables] = useState([]);

  // a few thoughts:
  // modules and cables should be a map { ...modules, 0: updatedModule }
  // cables should be a double map like in C++

  function addModule(moduleType) {
    const moduleId = Math.floor(Math.random() * 100) + 1; // TODO: bad
    count++;

    const module = { moduleId, moduleType };
    setModules((modules) => [...modules, module]);
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
    setCables((cables) => [...cables, cable]);
  }

  function moveCable(
    inModuleId,
    inPortId,
    outModuleId,
    outPortId,
    inXCoord,
    inYCoord,
    outXCoord,
    outYCoord
  ) {
    // filter that cable
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

    while (!element.classList.contains("rack")) {
      // TODO: padding, margin, border, outline
      // includes padding but not border
      const { borderLeftWidth, borderTopWidth } = getComputedStyle(element);
      xCoord += parseFloat(element.offsetLeft) + parseFloat(borderLeftWidth.slice(0, -2));
      yCoord += parseFloat(element.offsetTop) + parseFloat(borderTopWidth.slice(0, -2));
      element = element.offsetParent;
    }

    return { xCoord, yCoord };
  }

  let oldXCoord = 0;
  let oldYCoord = 0;
  let activeCableIndex = null;

  function handleMouseDown(event) {
    console.log(event.target);
    if (event.target.classList.contains("port")) {
      // and does not have cable already...
      // not the most "React" way...
      let { xCoord, yCoord } = calcRackCoords(event.target);
      xCoord += event.target.offsetWidth / 2;
      yCoord += event.target.offsetHeight / 2;

      console.log(xCoord, yCoord);

      addCable(0, 0, 0, 0, xCoord, yCoord, xCoord, yCoord);

      // actually maybe it's fine to set via state since you're still recording the old coords here
      const rack = event.target.closest(".rack");
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

    setCables((cables) => {
      // for dev, modify last cable
      const cable = {
        ...cables[cables.length - 1],
        outXCoord: cables[cables.length - 1].outXCoord + xOffset,
        outYCoord: cables[cables.length - 1].outYCoord + yOffset,
      };

      return [cable];
    });

    // if the mouse goes outside the window, cancel
    // dragging might break when scrolling simultaneously since clientX/Y are relative to viewport
  }

  function handleMouseUp(event) {
    const maybe = document.elementsFromPoint(event.clientX, event.clientY);
    let port = null;
    for (const element of maybe) {
      if (element.classList.contains("port")) {
        port = element;
        break;
      }
    }
    if (port) {
      // and does not have cable already...
      let { xCoord, yCoord } = calcRackCoords(port);
      xCoord += port.offsetWidth / 2;
      yCoord += port.offsetHeight / 2;

      setCables((cables) => {
        // for dev, modify last cable
        const cable = {
          ...cables[cables.length - 1],
          outXCoord: xCoord,
          outYCoord: yCoord,
        };

        return [cable];
      });

      const rack = event.target.closest(".rack");
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
    <>
      <button onClick={() => addModule(__TO_DEVICE)}>TO DEVICE</button>
      <button onClick={() => addModule(__OSCILLATOR)}>VCO</button>
      <div className="rack" onMouseDown={handleMouseDown}>
        {modules.map((module, i) => {
          const { moduleId, moduleType } = module;
          switch (moduleType) {
            case __TO_DEVICE:
              return <ToDeviceModule key={moduleId} moduleId={moduleId} />;
            case __FROM_DEVICE:
              return;
            case __OSCILLATOR:
              return (
                <OscillatorModule
                  key={moduleId}
                  moduleId={moduleId}
                  xCoord={200 * i}
                  yCoord={200}
                />
              );
            case __ENVELOPE:
              return;
            case __FILTER:
              return;
            case __AMPLIFIER:
              return;
            case __MIXER:
              return;
          }
        })}
        {cables.map((cable) => {
          const { inXCoord, inYCoord, outXCoord, outYCoord } = cable;
          return (
            <Cable
              key={0}
              inXCoord={inXCoord}
              inYCoord={inYCoord}
              outXCoord={outXCoord}
              outYCoord={outYCoord}
            />
          );
        })}
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
    </>
  );
}

export default Rack;
