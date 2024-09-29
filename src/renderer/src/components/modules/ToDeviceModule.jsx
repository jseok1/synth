import "../../assets/styles/OscillatorModule.css";

import { useEffect } from "react";
import { InPort } from "../Port";

function ToDeviceModule(props) {
  const { moduleId, xCoord, yCoord, setCables, calcCoords } = props;

  useEffect(() => {
    console.log(`api.addModule(moduleId: ${moduleId}, moduleType: __TO_DEVICE);`);
    api.addModule(moduleId, 0);
    return () => {
      console.log(`api.removeModule(moduleId: ${moduleId});`);
      api.removeModule(moduleId);
    };
  }, []);

  return (
    <div className="module module-outer to-device" style={{ top: yCoord, left: xCoord }}>
      <div className="module-inner">
        <div className="module-type">TO DEVICE</div>
        <div>{moduleId}</div>

        <div className="ports">
          <InPort
            moduleId={moduleId}
            portId={0}
            label="AUDIO"
            setCables={setCables}
            calcCoords={calcCoords}
          />
        </div>
      </div>
    </div>
  );
}

export default ToDeviceModule;
