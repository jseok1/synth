import "../../assets/styles/OscillatorModule.css";

import { useEffect, useState } from "react";
import Slider from "../Slider";
import { InPort, OutPort } from "../Port";

const __FREQ = 0;
const __FREQ_MOD_AMT = 1;
const __PUL_WIDTH = 2;
const __PUL_WIDTH_MOD_AMT = 3;

// TODO: will components being run twice lead to problems for C++?
function OscillatorModule(props) {
  const { moduleId, xCoord, yCoord, setCables, calcCoords } = props;

  const params = {};
  const handlers = {};

  [params[__FREQ], handlers[__FREQ]] = useState(8.175799 * Math.pow(2, 3));
  [params[__FREQ_MOD_AMT], handlers[__FREQ_MOD_AMT]] = useState(0.0);
  [params[__PUL_WIDTH], handlers[__PUL_WIDTH]] = useState(0.5);
  [params[__PUL_WIDTH_MOD_AMT], handlers[__PUL_WIDTH_MOD_AMT]] = useState(0.0);

  useEffect(() => {
    console.log(`api.addModule(moduleId: ${moduleId}, moduleType: __OSCILLATOR);`);
    api.addModule(moduleId, 2);
    return () => {
      console.log(`api.removeModule(moduleId: ${moduleId});`);
      api.removeModule(moduleId);
    };
  }, []);

  // is there a way to do this directly with event handlers actually?
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
          min={0}
          max={1000}
          value={params[__FREQ]}
          onChange={(event) => {
            // actually better if you can use state instead of event.target.value
            handlers[__FREQ](parseFloat(event.target.value));
          }}
        />
        <div>{params[__FREQ]}</div>
        <div>{moduleId}</div>

        <div className="ports">
          {/* TODO: __IN_PORT_... naming */}
          <InPort
            moduleId={moduleId}
            portId={0}
            label="FM"
            setCables={setCables}
            calcCoords={calcCoords}
          />
          <InPort
            moduleId={moduleId}
            portId={1}
            label="PWM"
            setCables={setCables}
            calcCoords={calcCoords}
          />
          <InPort
            moduleId={moduleId}
            portId={2}
            label="V/OCT"
            setCables={setCables}
            calcCoords={calcCoords}
          />
          <InPort
            moduleId={moduleId}
            portId={3}
            label="SYNC"
            setCables={setCables}
            calcCoords={calcCoords}
          />
        </div>

        <div className="ports">
          {/* TODO: __OUT_PORT_... naming */}
          <OutPort
            moduleId={moduleId}
            portId={0}
            label="SIN"
            setCables={setCables}
            calcCoords={calcCoords}
          />
          <OutPort
            moduleId={moduleId}
            portId={1}
            label="TRI"
            setCables={setCables}
            calcCoords={calcCoords}
          />
          <OutPort
            moduleId={moduleId}
            portId={2}
            label="SAW"
            setCables={setCables}
            calcCoords={calcCoords}
          />
          <OutPort
            moduleId={moduleId}
            portId={3}
            label="SQR"
            setCables={setCables}
            calcCoords={calcCoords}
          />
        </div>
      </div>
    </div>
  );
}

export default OscillatorModule;
