import { useEffect, useState } from "react";

import OscillatorModule from "./OscillatorModule";

function Rack() {
  const [modules, setModules] = useState([]);

  function addModule(moduleType) {
    const moduleId = modules.size + 1; // TODO: better
    let module;
    if (moduleType == 0) {
      module = <OscillatorModule moduleId={moduleId} />; // does this instantiate a new one each time?
      // immediately after instantiation, call updateParam to sync backend to frontend
    }

    setModules([...modules, module]);
    api.addModule(moduleId, moduleType);  // return object with params
  }

  useEffect(() => {
    addModule(0);
    // api.addCable(0, 0, 1, 1);
    // api.startStream();
  }, []);

  return (
    <>
      <div>{modules}</div>
    </>
  );
}

export default Rack;
