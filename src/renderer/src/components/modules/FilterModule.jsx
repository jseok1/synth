import { useEffect, useState } from "react";
import Slider from "../Slider";
import { InPort, OutPort } from "../Port";

const __FREQ_CUT = 0;
const __FREQ_CUT_MOD_AMT = 1;
const __RES = 2;
const __RES_MOD_AMT = 3;

function FilterModule(props) {
  const { moduleId, xCoord, yCoord, setCables, calcCoords } = props;

  const params = {};
  const handlers = {};

  [params[__FREQ_CUT], handlers[__FREQ_CUT]] = useState(0.0);
  [params[__FREQ_CUT_MOD_AMT], handlers[__FREQ_CUT_MOD_AMT]] = useState(0.0);
  [params[__RES], handlers[__RES]] = useState(0.0);
  [params[__RES_MOD_AMT], handlers[__RES_MOD_AMT]] = useState(0.0);

  useEffect(() => {
    console.log(`api.addModule(moduleId: ${moduleId}, moduleType: __FILTER);`);
    api.addModule(moduleId, 4);
    return () => {
      console.log(`api.removeModule(moduleId: ${moduleId});`);
      api.removeModule(moduleId);
    };
  }, []);

  useEffect(() => {
    api.updateParam(moduleId, __FREQ_CUT, params[__FREQ_CUT]);
  }, [params[__FREQ_CUT]]);

  useEffect(() => {
    api.updateParam(moduleId, __FREQ_CUT_MOD_AMT, params[__FREQ_CUT_MOD_AMT]);
  }, [params[__FREQ_CUT_MOD_AMT]]);

  useEffect(() => {
    api.updateParam(moduleId, __RES, params[__RES]);
  }, [params[__RES]]);

  useEffect(() => {
    api.updateParam(moduleId, __RES_MOD_AMT, params[__RES_MOD_AMT]);
  }, [params[__RES_MOD_AMT]]);

  return (
    <div className="module module-outer filter" style={{ top: yCoord, left: xCoord }}>
      <div className="module-inner">
        <div className="module-type">VCF</div>
        <Slider
          label="FREQ CUTOFF"
          min={0}
          max={1000}
          value={params[__FREQ_CUT]}
          onChange={(event) => {
            // actually better if you can use state instead of event.target.value
            handlers[__FREQ_CUT](parseFloat(event.target.value));
          }}
        />
        <div>{params[__FREQ_CUT]}</div>
        <div>{moduleId}</div>

        <div className="ports">
          {/* TODO: __IN_PORT_... naming */}
          <InPort
            moduleId={moduleId}
            portId={0}
            label="CUTM"
            setCables={setCables}
            calcCoords={calcCoords}
          />
          <InPort
            moduleId={moduleId}
            portId={1}
            label="RESM"
            setCables={setCables}
            calcCoords={calcCoords}
          />
          <InPort
            moduleId={moduleId}
            portId={2}
            label="IN"
            setCables={setCables}
            calcCoords={calcCoords}
          />
        </div>

        <div className="ports">
          {/* TODO: __OUT_PORT_... naming */}
          <OutPort
            moduleId={moduleId}
            portId={0}
            label="OUT"
            setCables={setCables}
            calcCoords={calcCoords}
          />
        </div>
      </div>
    </div>
  );
}

export default FilterModule;
