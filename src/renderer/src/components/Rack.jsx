import "../assets/styles/Rack.css";

import { useEffect, useState } from "react";

import ToDeviceModule from "./ToDeviceModule";
import OscillatorModule from "./OscillatorModule";

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

  function addModule(moduleType) {
    const moduleId = Math.floor(Math.random() * 100) + 1;
    // const moduleId = count;
    count++;

    // do subcomponents keep their state?
    // If the key for a component remains the same across renders, React reuses the same component instance and its state

    const module = { moduleId, moduleType };
    setModules((modules) => [...modules, module]);
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

  return (
    <>
      <button onClick={() => addModule(__TO_DEVICE)}>TO DEVICE</button>
      <button onClick={() => addModule(__OSCILLATOR)}>VCO</button>
      <div className="rack">
        {modules.map((module) => {
          const { moduleId, moduleType } = module;
          switch (moduleType) {
            case __TO_DEVICE:
              return <ToDeviceModule key={moduleId} moduleId={moduleId} />;
            case __FROM_DEVICE:
              return;
            case __OSCILLATOR:
              return <OscillatorModule key={moduleId} moduleId={moduleId} />;
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
      </div>
    </>
  );
}

export default Rack;
