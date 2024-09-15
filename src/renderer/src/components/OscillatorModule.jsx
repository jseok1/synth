import "../assets/styles/OscillatorModule.css";

import { useEffect, useState } from "react";
import Slider from "./Slider";
import InPort from "./InPort";

const __FREQ = 0;
const __FREQ_MOD_AMT = 1;
const __PUL_WIDTH = 2;
const __PUL_WIDTH_MOD_AMT = 3;

// TODO: will components being run twice lead to problems for C++?
function OscillatorModule(props) {
  const { moduleId, xCoord, yCoord } = props;

  const params = {};
  const handlers = {};

  [params[__FREQ], handlers[__FREQ]] = useState(8.175799 * Math.pow(2, 3));
  [params[__FREQ_MOD_AMT], handlers[__FREQ_MOD_AMT]] = useState(0.0);
  [params[__PUL_WIDTH], handlers[__PUL_WIDTH]] = useState(0.5);
  [params[__PUL_WIDTH_MOD_AMT], handlers[__PUL_WIDTH_MOD_AMT]] = useState(0.0);

  useEffect(() => {
    console.log(`api.addModule(${moduleId}, __OSCILLATOR);`);
    api.addModule(moduleId, 2);
    return () => {
      console.log(`api.removeModule(${moduleId});`);
      api.removeModule(moduleId);
    };
  }, []);

  useEffect(() => {
    api.updateParam(moduleId, __FREQ, params[__FREQ]);
  }, [params[__FREQ]]);

  useEffect(() => {
    api.updateParam(moduleId, __FREQ_MOD_AMT, params[__FREQ_MOD_AMT]);
  }, [params[__FREQ_MOD_AMT]]);

  useEffect(() => {
    api.updateParam(moduleId, __PUL_WIDTH, params[__PUL_WIDTH]);
  }, [params[__PUL_WIDTH]]);

  useEffect(() => {
    api.updateParam(moduleId, __PUL_WIDTH_MOD_AMT, params[__PUL_WIDTH_MOD_AMT]);
  }, [params[__PUL_WIDTH_MOD_AMT]]);

  return (
    <div className="module module-outer oscillator" style={{ top: yCoord, left: xCoord }}>
      <div className="module-inner">
        <div className="module-type">VCO</div>
        <Slider
          label="FREQ"
          min="0"
          max="1000"
          onChange={(event) => {
            handlers[__FREQ](parseFloat(event.target.value));
          }}
        />
        <div>{params[__FREQ]}</div>
        <div>{moduleId}</div>

        <div className="out">
          <InPort xCoord={xCoord} yCoord={yCoord} />
          <InPort xCoord={xCoord} yCoord={yCoord} />
          <InPort xCoord={xCoord} yCoord={yCoord} />
          <InPort xCoord={xCoord} yCoord={yCoord} />
        </div>
      </div>
    </div>
  );
}

export default OscillatorModule;
