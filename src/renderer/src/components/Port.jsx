import { useRef } from "react";

function InPort(props) {
  const { moduleId, portId, label, setCables, calcCoords } = props;
  const inPortElement = useRef(null);

  function handleMouseDown(event) {
    let { xCoord, yCoord } = calcCoords(inPortElement.current);
    xCoord += inPortElement.current.offsetWidth / 2;
    yCoord += inPortElement.current.offsetHeight / 2;

    setCables((cables) => {
      cables = { ...cables };

      let cableId;
      let maxZCoordLocal = 0; // TODO: maybe better mechanism for z-index that doesn't rely on incrementing unboundedly
      let maxZCoordGlobal = 0;
      for (const cable of Object.values(cables)) {
        if (
          cable.inModuleId === moduleId &&
          cable.inPortId === portId &&
          cable.zCoord > maxZCoordLocal
        ) {
          cableId = cable.cableId;
          maxZCoordLocal = cable.zCoord;
        }
        if (cable.zCoord > maxZCoordGlobal) {
          maxZCoordGlobal = cable.zCoord;
        }
      }

      if (cableId) {
        const cable = cables[cableId];
        cables[cableId] = {
          ...cable,
          inModuleId: null,
          inPortId: null,
          inXCoord: event.clientX,
          inYCoord: event.clientY,
          zCoord: maxZCoordGlobal + 1,
          inIsDragging: true,
        };
      } else {
        do {
          cableId = Math.floor(Math.random() * 1000) + 1;
        } while (cableId in cables);
        cables[cableId] = {
          cableId,
          inModuleId: moduleId,
          inPortId: portId,
          outModuleId: null,
          outPortId: null,
          inXCoord: xCoord,
          inYCoord: yCoord,
          outXCoord: event.clientX,
          outYCoord: event.clientY,
          zCoord: maxZCoordGlobal + 1,
          inIsDragging: false,
          outIsDragging: true,
        };
      }

      return cables;
    });
  }

  function handleMouseUp(event) {
    let { xCoord, yCoord } = calcCoords(inPortElement.current);
    xCoord += inPortElement.current.offsetWidth / 2;
    yCoord += inPortElement.current.offsetHeight / 2;

    setCables((cables) => {
      cables = { ...cables };

      for (const [cableId, cable] of Object.entries(cables)) {
        if (cable.inIsDragging) {
          cables[cableId] = {
            ...cable,
            inModuleId: moduleId,
            inPortId: portId,
            inXCoord: xCoord,
            inYCoord: yCoord,
            inIsDragging: false,
          };
        }
      }

      return cables;
    });
  }

  return (
    <div className="port in-port" onMouseDown={handleMouseDown} onMouseUp={handleMouseUp}>
      <div className="port-icon" ref={inPortElement}>
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
          <circle cx="50" cy="50" r="45" stroke="#38383b" strokeWidth="5" fill="#e4e4e4" />
          <circle cx="50" cy="50" r="36.5" stroke="#38383b" strokeWidth="5" fill="#e4e4e4" />
          <circle cx="50" cy="50" r="25" fill="#38383b" />
        </svg>
      </div>
      <div className="port-label">{label}</div>
    </div>
  );
}

function OutPort(props) {
  const { moduleId, portId, label, setCables, calcCoords } = props;
  const outPortElement = useRef(null);

  function handleMouseDown(event) {
    let { xCoord, yCoord } = calcCoords(outPortElement.current);
    xCoord += outPortElement.current.offsetWidth / 2;
    yCoord += outPortElement.current.offsetHeight / 2;

    setCables((cables) => {
      cables = { ...cables };

      let cableId;
      let maxZCoordLocal = 0;
      let maxZCoordGlobal = 0;
      for (const cable of Object.values(cables)) {
        if (
          cable.outModuleId === moduleId &&
          cable.outPortId === portId &&
          cable.zCoord > maxZCoordLocal
        ) {
          cableId = cable.cableId;
          maxZCoordLocal = cable.zCoord;
        }
        if (cable.zCoord > maxZCoordGlobal) {
          maxZCoordGlobal = cable.zCoord;
        }
      }

      if (cableId) {
        const cable = cables[cableId];
        cables[cableId] = {
          ...cable,
          outModuleId: null,
          outPortId: null,
          outXCoord: event.clientX,
          outYCoord: event.clientY,
          zCoord: maxZCoordGlobal + 1,
          outIsDragging: true,
        };
      } else {
        do {
          cableId = Math.floor(Math.random() * 1000) + 1;
        } while (cableId in cables);
        cables[cableId] = {
          cableId,
          inModuleId: null,
          inPortId: null,
          outModuleId: moduleId,
          outPortId: portId,
          inXCoord: event.clientX,
          inYCoord: event.clientY,
          outXCoord: xCoord,
          outYCoord: yCoord,
          zCoord: maxZCoordGlobal + 1,
          inIsDragging: true,
          outIsDragging: false,
        };
      }

      return cables;
    });
  }

  function handleMouseUp(event) {
    let { xCoord, yCoord } = calcCoords(outPortElement.current);
    xCoord += outPortElement.current.offsetWidth / 2;
    yCoord += outPortElement.current.offsetHeight / 2;

    setCables((cables) => {
      cables = { ...cables };

      for (const [cableId, cable] of Object.entries(cables)) {
        if (cable.outIsDragging) {
          cables[cableId] = {
            ...cable,
            outModuleId: moduleId,
            outPortId: portId,
            outXCoord: xCoord,
            outYCoord: yCoord,
            outIsDragging: false,
          };
        }
      }

      return cables;
    });
  }

  return (
    <div className="port out-port" onMouseDown={handleMouseDown} onMouseUp={handleMouseUp}>
      <div className="port-icon" ref={outPortElement}>
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
          <circle cx="50" cy="50" r="45" stroke="#38383b" strokeWidth="5" fill="#e4e4e4" />
          <circle cx="50" cy="50" r="36.5" stroke="#38383b" strokeWidth="5" fill="#e4e4e4" />
          <circle cx="50" cy="50" r="25" fill="#38383b" />
        </svg>
      </div>
      <div className="port-label">{label}</div>
    </div>
  );
}

export { InPort, OutPort };
