<script lang="ts">
  let { cable } = $props();

  const { inXCoordControl, inYCoordControl, outXCoordControl, outYCoordControl } = $derived.by(
    () => {
      const xRange = cable.inPlug.xCoord - cable.outPlug.xCoord;
      const yRange = Math.abs(cable.inPlug.yCoord - cable.outPlug.yCoord);

      const xAdjust = xRange * 0.2;
      const yAdjust = Math.abs(xRange) * 0.2 + yRange * 0.2; // TODO: play around with weights

      const inXCoordControl = cable.inPlug.xCoord - xAdjust;
      const inYCoordControl = Math.max(cable.inPlug.yCoord + yAdjust, cable.outPlug.yCoord + yAdjust);
      const outXCoordControl = cable.outPlug.xCoord + xAdjust;
      const outYCoordControl = Math.max(cable.inPlug.yCoord + yAdjust, cable.outPlug.yCoord + yAdjust);

      return { inXCoordControl, inYCoordControl, outXCoordControl, outYCoordControl };
    },
  );

  $effect(() => {

    return () => {
      // removpe cable
    }
  });

  // edit <g>
</script>

<div class="cable" style:z-index={cable.zCoord}>
  <svg xmlns="http://www.w3.org/2000/svg">
    <path
      d={`M ${cable.inPlug.xCoord} ${cable.inPlug.yCoord} C ${inXCoordControl} ${inYCoordControl}, ${outXCoordControl} ${outYCoordControl}, ${cable.outPlug.xCoord} ${cable.outPlug.yCoord}`}
      stroke={cable.color}
      stroke-width="5"
      fill="none"
      opacity="0.5"
    />
    <!-- are there px units? -->
    <g fill={cable.color}>
      <circle cx={cable.inPlug.xCoord} cy={cable.inPlug.yCoord} r="10" />
      <circle cx={cable.outPlug.xCoord} cy={cable.outPlug.yCoord} r="10" />
      <g opacity="0.2">
        <circle cx={inXCoordControl} cy={inYCoordControl} r="10" />
        <circle cx={outXCoordControl} cy={outYCoordControl} r="10" />
      </g>
    </g>
  </svg>
</div>

<style>
  .cable {
    position: absolute;
    width: 100%;
    height: 100%;
    pointer-events: none;
    overflow: hidden;
  }
</style>
