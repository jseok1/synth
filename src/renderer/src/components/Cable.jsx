import { useEffect } from "react";

function Cable(props) {
  const { inModuleId, inPortId, outModuleId, outPortId, inXCoord, inYCoord, outXCoord, outYCoord } =
    props;

  useEffect(() => {
    if (inModuleId !== null && inPortId !== null && outModuleId !== null && outPortId !== null) {
      console.log(
        `api.addCable(inModuleId: ${inModuleId}, inPortId: ${inPortId}, outModuleId: ${outModuleId}, outPortId: ${outPortId});`
      );
      api.addCable(inModuleId, inPortId, outModuleId, outPortId);
      return () => {
        console.log(`api.removeCable(inModuleId: ${inModuleId}, inPortId: ${inPortId});`);
        api.removeCable(inModuleId, inPortId);
      };
    }
  }, [inModuleId, inPortId, outModuleId, outPortId]);

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

  return (
    <div className="cable">
      <svg xmlns="http://www.w3.org/2000/svg">
        <path
          d={`M ${inXCoord} ${inYCoord} C ${inXCoordControl} ${inYCoordControl}, ${outXCoordControl} ${outYCoordControl}, ${outXCoord} ${outYCoord}`}
          stroke="orange"
          strokeWidth="5"
          fill="none"
          opacity="0.5"
        />
        {/* are there px units? */}
        <g fill="orange">
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
