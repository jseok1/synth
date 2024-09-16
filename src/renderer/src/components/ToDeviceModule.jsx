import "../assets/styles/OscillatorModule.css";

import { useEffect } from "react";
import { InPort } from "./Port";

function ToDeviceModule(props) {
  const { moduleId, xCoord, yCoord } = props;

  useEffect(() => {
    console.log(`api.addModule(${moduleId}, __TO_DEVICE);`);
    api.addModule(moduleId, 0);
    return () => {
      console.log(`api.removeModule(${moduleId});`);
      api.removeModule(moduleId);
    };
  }, []);

  return (
    <div className="module to-device">
      <div className="module-type">TO DEVICE</div>
      <div>{moduleId}</div>

      <div className="out">
        <InPort />
      </div>
    </div>
  );
}

export default ToDeviceModule;
