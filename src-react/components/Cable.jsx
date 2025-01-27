import { useEffect } from "react";

function Cable(props) {
  const {
    cableId,
    inModuleId,
    inPortType,
    outModuleId,
    outPortType,
    inXCoord,
    inYCoord,
    outXCoord,
    outYCoord,
    zCoord,
  } = props;

  useEffect(() => {
    if (inModuleId !== null && inPortType !== null && outModuleId !== null && outPortType !== null) {
      console.log(
        `api.addCable(inModuleId: ${inModuleId}, inPortType: ${inPortType}, outModuleId: ${outModuleId}, outPortType: ${outPortType});`
      );
      api.addCable(inModuleId, inPortType, outModuleId, outPortType);
      return () => {
        console.log(`api.removeCable(inModuleId: ${inModuleId}, inPortType: ${inPortType});`);
        api.removeCable(inModuleId, inPortType);
      };
    }
  }, [inModuleId, inPortType, outModuleId, outPortType]);

  const xRange = inXCoord - outXCoord;
  const yRange = Math.abs(inYCoord - outYCoord);

  const xAdjust = xRange * 0.2;
  const yAdjust = Math.abs(xRange) * 0.2 + yRange * 0.2; // TODO: play around with weights

  const inXCoordControl = inXCoord - xAdjust;
  let inYCoordControl = inYCoord + yAdjust;
  const outXCoordControl = outXCoord + xAdjust;
  let outYCoordControl = outYCoord + yAdjust;
  inYCoordControl = Math.max(inYCoordControl, outYCoordControl);
  outYCoordControl = inYCoordControl;
  // edit <g>

  const color = [
    "hsl(40 90% 70%)",
    "hsl(0 90% 70%)",
    "hsl(120, 90%, 70%)",
    "hsl(220, 90%, 70%)",
    "hsl(300, 90%, 70%)",
  ][cableId % 5];

  return (
    <div className="cable" style={{ zIndex: zCoord }}>
      <svg xmlns="http://www.w3.org/2000/svg">
        <path
          d={`M ${inXCoord} ${inYCoord} C ${inXCoordControl} ${inYCoordControl}, ${outXCoordControl} ${outYCoordControl}, ${outXCoord} ${outYCoord}`}
          stroke={color}
          strokeWidth="5"
          fill="none"
          opacity="0.5"
        />
        {/* are there px units? */}
        <g fill={color}>
          <circle cx={inXCoord} cy={inYCoord} r="10" />
          <circle cx={outXCoord} cy={outYCoord} r="10" />
          <g opacity="0.2">
            <circle cx={inXCoordControl} cy={inYCoordControl} r="10" />
            <circle cx={outXCoordControl} cy={outYCoordControl} r="10" />
          </g>
        </g>
      </svg>
    </div>
  );
}

export default Cable;
