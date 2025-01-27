<script lang="ts">
  import { getContext } from "svelte";

  let { module, outPortId, label, cables } = $props();

  let outPortElement: HTMLElement;

  const {
    calcCoords,
    addCable,
    dragInPlug,
    dragOutPlug,
    connectOutPlugToOutPort,
    disconnectOutPlugFromOutPort,
  } = getContext("rack");

  function handleMouseDown(event: MouseEvent): void {
    const { xCoord, yCoord } = calcCoords(outPortElement);

    let cableId = module.outPorts[outPortId].cableIds.at(-1);
    if (cableId) {
      disconnectOutPlugFromOutPort(cableId);
      dragOutPlug(cableId, event.clientX, event.clientY, false);
    } else {
      cableId = addCable();
      connectOutPlugToOutPort(cableId, module.moduleId, outPortId);
      dragInPlug(cableId, event.clientX, event.clientY, false);
      dragOutPlug(cableId, xCoord, yCoord, true);
    }

    event.stopPropagation();
  }

  function handleMouseUp(event: MouseEvent): void {
    const { xCoord, yCoord } = calcCoords(outPortElement);

    for (const [cableId, cable] of Object.entries(cables)) {
      if (!cable.outPlug.isDropped) {
        connectOutPlugToOutPort(cableId, module.moduleId, outPortId);
        dragOutPlug(cableId, xCoord, yCoord, true);
      }
    }
  }
</script>

<!-- svelte-ignore a11y_no_static_element_interactions -->
<div class="port out-port" onmousedown={handleMouseDown} onmouseup={handleMouseUp}>
  <div class="port-icon" bind:this={outPortElement}>
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
      <circle cx="50" cy="50" r="45" stroke="#38383b" stroke-width="5" fill="#e4e4e4" />
      <circle cx="50" cy="50" r="36.5" stroke="#38383b" stroke-width="5" fill="#e4e4e4" />
      <circle cx="50" cy="50" r="25" fill="#38383b" />
    </svg>
  </div>
  <div class="port-label">{label}</div>
</div>

<style>
  .port {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 40px;
    padding: 2.5px;
    border-radius: 10px;
  }
  .port * {
    pointer-events: none;
  }
  .port.out-port {
    background-color: var(--color-black);
    color: var(--color-white);
  }
  .port-icon {
    width: 30px;
    height: 30px;
    margin-bottom: 2.5px;
  }
  .port-label {
    font-size: var(--font-size-xs);
    padding: 2.5px;
  }
</style>
