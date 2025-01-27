import "../../assets/styles/OscillatorModule.css";

import { ReactElement, useEffect, useState } from "react";
import Slider from "../Slider";
import { InPort, OutPort } from "../Port";
import Module from "../Module";

import Rack from "../Rack";

enum OscillatorParam {
  __FREQ,
  __FREQ_MOD_AMT,
  __PUL_WIDTH,
  __PUL_WIDTH_MOD_AMT,
}

enum OscillatorInPort {
  __FREQ_MOD,
  __PUL_WIDTH_MOD,
  __VOLT_PER_OCT,
  __SYNC,
}

enum OscillatorOutPort {
  __SIN,
  __TRI,
  __SAW,
  __SQR,
  __PUL,
}

interface OscillatorModuleProps {
  moduleId: number;
  xCoord: number;
  yCoord: number;
  isDragging: boolean;
  setRack: React.Dispatch<React.SetStateAction<Rack>>;
  calcCoords: (element: HTMLElement) => { xCoord: number; yCoord: number };
}

// TODO: will components being run twice lead to problems for C++?
function OscillatorModule(props: OscillatorModuleProps): ReactElement<any, any> | null {
  const { moduleId, xCoord, yCoord, isDragging, setRack, calcCoords } = props;

  const param = {};
  const updateParam = {};

  [param[OscillatorParam.__FREQ], updateParam[OscillatorParam.__FREQ]] = useState(
    8.175799 * Math.pow(2, 3)
  );
  [param[OscillatorParam.__FREQ_MOD_AMT], updateParam[OscillatorParam.__FREQ_MOD_AMT]] =
    useState(0.0);
  [param[OscillatorParam.__PUL_WIDTH], updateParam[OscillatorParam.__PUL_WIDTH]] = useState(0.5);
  [param[OscillatorParam.__PUL_WIDTH_MOD_AMT], updateParam[OscillatorParam.__PUL_WIDTH_MOD_AMT]] =
    useState(0.0);

  useEffect(() => {
    console.log(`api.addModule(moduleId: ${moduleId}, moduleType: ModuleType.__OSCILLATOR);`);
    window.api.engine.addModule(moduleId, 2);
    return () => {
      console.log(`api.removeModule(moduleId: ${moduleId});`);
      window.api.engine.removeModule(moduleId);
    };
  }, []);

  // is there a way to do this directly with event updateParam actually?
  useEffect(() => {
    window.api.engine.updateParam(moduleId, OscillatorParam.__FREQ, param[OscillatorParam.__FREQ]);
  }, [param[OscillatorParam.__FREQ]]);

  useEffect(() => {
    window.api.engine.updateParam(
      moduleId,
      OscillatorParam.__FREQ_MOD_AMT,
      param[OscillatorParam.__FREQ_MOD_AMT]
    );
  }, [param[OscillatorParam.__FREQ_MOD_AMT]]);

  useEffect(() => {
    window.api.engine.updateParam(
      moduleId,
      OscillatorParam.__PUL_WIDTH,
      param[OscillatorParam.__PUL_WIDTH]
    );
  }, [param[OscillatorParam.__PUL_WIDTH]]);

  useEffect(() => {
    window.api.engine.updateParam(
      moduleId,
      OscillatorParam.__PUL_WIDTH_MOD_AMT,
      param[OscillatorParam.__PUL_WIDTH_MOD_AMT]
    );
  }, [param[OscillatorParam.__PUL_WIDTH_MOD_AMT]]);

  return (
    <Module moduleId={moduleId} isDragging={isDragging} setRack={setRack}>
      <div
        className="module module-outer oscillator"
        style={{ top: yCoord, left: xCoord, width: OscillatorWidth, height: OscillatorHeight }}
      >
        <div className="module-inner">
          <div className="module-type">VCO</div>
          <Slider
            label="FREQ"
            min={0}
            max={1000}
            value={param[OscillatorParam.__FREQ]}
            onChange={(event) => {
              // actually better if you can use state instead of event.target.value
              updateParam[OscillatorParam.__FREQ](parseFloat(event.target.value));
            }}
          />
          <div>{param[OscillatorParam.__FREQ]}</div>
          <div>{moduleId}</div>

          <div className="ports">
            <InPort
              moduleId={moduleId}
              portId={OscillatorInPort.__FREQ_MOD}
              label="FM"
              setRack={setRack}
              calcCoords={calcCoords}
            />
            <InPort
              moduleId={moduleId}
              portId={OscillatorInPort.__PUL_WIDTH_MOD}
              label="PWM"
              setRack={setRack}
              calcCoords={calcCoords}
            />
            <InPort
              moduleId={moduleId}
              portId={OscillatorInPort.__VOLT_PER_OCT}
              label="V/OCT"
              setRack={setRack}
              calcCoords={calcCoords}
            />
            <InPort
              moduleId={moduleId}
              portId={OscillatorInPort.__SYNC}
              label="SYNC"
              setRack={setRack}
              calcCoords={calcCoords}
            />
          </div>

          <div className="ports">
            <OutPort
              moduleId={moduleId}
              portId={OscillatorOutPort.__SIN}
              label="SIN"
              setRack={setRack}
              calcCoords={calcCoords}
            />
            <OutPort
              moduleId={moduleId}
              portId={OscillatorOutPort.__TRI}
              label="TRI"
              setRack={setRack}
              calcCoords={calcCoords}
            />
            <OutPort
              moduleId={moduleId}
              portId={OscillatorOutPort.__SAW}
              label="SAW"
              setRack={setRack}
              calcCoords={calcCoords}
            />
            <OutPort
              moduleId={moduleId}
              portId={OscillatorOutPort.__SQR}
              label="SQR"
              setRack={setRack}
              calcCoords={calcCoords}
            />
          </div>
        </div>
      </div>
    </Module>
  );
}

export default OscillatorModule;

export const OscillatorInPorts: OscillatorInPort[] = [
  OscillatorInPort.__FREQ_MOD,
  OscillatorInPort.__PUL_WIDTH_MOD,
  OscillatorInPort.__VOLT_PER_OCT,
  OscillatorInPort.__SYNC,
];
export const OscillatorOutPorts: OscillatorOutPort[] = [
  OscillatorOutPort.__SIN,
  OscillatorOutPort.__TRI,
  OscillatorOutPort.__SAW,
  OscillatorOutPort.__SQR,
  OscillatorOutPort.__PUL,
];

export const OscillatorWidth = 50 * 4;
export const OscillatorHeight = 50 * 8;
