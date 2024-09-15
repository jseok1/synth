function Cable(props) {
  const { inXCoord, inYCoord, outXCoord, outYCoord } = props;

  // sliders are integral, so *100 then / 100 to get 2 decimals of precision

  const xRange = inXCoord - outXCoord;
  const yRange = Math.abs(inYCoord - outYCoord);

  const xAdjust = xRange * 0.2;
  const yAdjust = xRange * 0.2 + yRange * 0.2; // TODO: play around with weights

  const inXCoordControl = inXCoord - xAdjust;
  let inYCoordControl = inYCoord - yAdjust;
  const outXCoordControl = outXCoord + xAdjust;
  let outYCoordControl = outYCoord - yAdjust;
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
