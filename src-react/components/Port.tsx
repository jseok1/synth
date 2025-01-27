import { ReactElement, useRef } from "react";
import Rack from "./Rack";

import { v4 as uuid } from "uuid";

interface InPortProps {
  moduleId: string;
  portType: number;
  label: string;
  setRack: React.Dispatch<React.SetStateAction<Rack>>;
  calcCoords: (element: HTMLElement) => { xCoord: number; yCoord: number };
  addCable: (
    { modules, cables }: Rack,
    inModuleId: string,
    inPortType: number,
    outModuleId: string,
    outPortType: number,
    inXCoord: number,
    inYCoord: number,
    outXCoord: number,
    outYCoord: number,
    zCoord: number
  ) => Rack;
}

function InPort(props: InPortProps): ReactElement | null {
  const { moduleId, portType, label, setRack, calcCoords, addCable } = props;
  const inPortElement = useRef<HTMLDivElement>(null);

  function handleMouseDown(event: MouseEvent): void {
    let { xCoord, yCoord } = calcCoords(inPortElement.current);
    xCoord += inPortElement.current.offsetWidth / 2;
    yCoord += inPortElement.current.offsetHeight / 2;

    setRack(({ modules, cables }: Rack): Rack => {
      modules = { ...modules };
      cables = { ...cables };

      let cableId = modules[moduleId].inPorts[portType].cableId;
      if (cableId) {
        modules[moduleId].inPorts[portType].cableId = "";

        cables[cableId] = {
          ...cables[cableId],
          inModuleId: "",
          inPortType: 0,
          inXCoord: event.clientX,
          inYCoord: event.clientY,
          inIsDraggable: true,
        };
      } else {
        modules[moduleId].inPorts[portType].cableId = cableId;
        ({ modules, cables } = addCable(
          { modules, cables },
          moduleId,
          portType,
          "",
          0,
          xCoord,
          yCoord,
          event.clientX,
          event.clientY,
          0
        ));
      }

      return { modules, cables };
    });

    event.stopPropagation();
  }

  function handleMouseUp(event) {
    let { xCoord, yCoord } = calcCoords(inPortElement.current);
    xCoord += inPortElement.current.offsetWidth / 2;
    yCoord += inPortElement.current.offsetHeight / 2;

    setRack(({ modules, cables }) => {
      cables = { ...cables };

      for (const [cableId, cable] of Object.entries(cables)) {
        if (cable.inIsDraggable) {
          cables[cableId] = {
            ...cable,
            inModuleId: moduleId,
            inPortType: portType,
            inXCoord: xCoord,
            inYCoord: yCoord,
            inIsDraggable: false,
          };
        }
      }

      return { modules, cables };
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
  const { moduleId, portType, label, setRack, calcCoords } = props;
  const outPortElement = useRef(null);

  function handleMouseDown(event) {
    let { xCoord, yCoord } = calcCoords(outPortElement.current);
    xCoord += outPortElement.current.offsetWidth / 2;
    yCoord += outPortElement.current.offsetHeight / 2;

    setRack(({ modules, cables }) => {
      cables = { ...cables };

      let cableId;
      let maxZCoordLocal = 0;
      let maxZCoordGlobal = 0;
      for (const cable of Object.values(cables)) {
        if (
          cable.outModuleId === moduleId &&
          cable.outPortType === portType &&
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
        modules[moduleId].outPorts[portType].cableId = null;

        const cable = cables[cableId];
        cables[cableId] = {
          ...cable,
          outModuleId: null,
          outPortType: null,
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
          inPortType: null,
          outModuleId: moduleId,
          outPortType: portType,
          inXCoord: event.clientX,
          inYCoord: event.clientY,
          outXCoord: xCoord,
          outYCoord: yCoord,
          zCoord: maxZCoordGlobal + 1,
          inIsDraggable: true,
          outIsDragging: false,
        };

        modules[moduleId].outPorts[portType].cableId = cableId;
      }

      return { modules, cables };
    });

    event.stopPropagation();
  }

  function handleMouseUp(event) {
    let { xCoord, yCoord } = calcCoords(outPortElement.current);
    xCoord += outPortElement.current.offsetWidth / 2;
    yCoord += outPortElement.current.offsetHeight / 2;

    setRack(({ modules, cables }) => {
      cables = { ...cables };

      for (const [cableId, cable] of Object.entries(cables)) {
        if (cable.outIsDragging) {
          cables[cableId] = {
            ...cable,
            outModuleId: moduleId,
            outPortType: portType,
            outXCoord: xCoord,
            outYCoord: yCoord,
            outIsDragging: false,
          };
        }
      }

      return { modules, cables };
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
