<script lang="ts">
  import { setContext } from "svelte";
  import Cable from "./Cable.svelte";
  import OscillatorModule from "./modules/OscillatorModule.svelte";

  import { v4 as uuid } from "uuid";

  const Modules = {
    [ModuleType.__TO_DEVICE]: OscillatorModule,
    [ModuleType.__FROM_DEVICE]: OscillatorModule,
    [ModuleType.__OSCILLATOR]: OscillatorModule,
    [ModuleType.__ENVELOPE]: OscillatorModule,
    [ModuleType.__FILTER]: OscillatorModule,
    [ModuleType.__AMPLIFIER]: OscillatorModule,
    [ModuleType.__MIXER]: OscillatorModule,
  };

  const unit = {
    width: 50,
    height: 50 * 8,
  } as const;

  const dimensions = {
    [ModuleType.__TO_DEVICE]: { width: unit.width * 4, height: unit.height },
    [ModuleType.__FROM_DEVICE]: { width: unit.width * 4, height: unit.height },
    [ModuleType.__OSCILLATOR]: { width: unit.width * 4, height: unit.height },
    [ModuleType.__ENVELOPE]: { width: unit.width * 4, height: unit.height },
    [ModuleType.__FILTER]: { width: unit.width * 4, height: unit.height },
    [ModuleType.__AMPLIFIER]: { width: unit.width * 4, height: unit.height },
    [ModuleType.__MIXER]: { width: unit.width * 4, height: unit.height },
  };

  let { modules, cables } = $state<Rack>({ modules: {}, cables: {} });
    let onMouseMove: ((xOffset: number, yOffset; number) => void) | null = null;
    let onMouseUp: ((xOffset: number, yOffset; number) => void) | null = null;

  let rackElement: HTMLElement;

  function calcCoords(element: HTMLElement): { xCoord: number; yCoord: number } {
    let xCoord = element.offsetWidth / 2;
    let yCoord = element.offsetHeight / 2;

    while (element && element !== rackElement) {
      // TODO: padding, margin, border, outline
      // includes padding but not border
      const { borderLeftWidth, borderTopWidth } = getComputedStyle(element);
      xCoord += element.offsetLeft + parseFloat(borderLeftWidth);
      yCoord += element.offsetTop + parseFloat(borderTopWidth);
      element = element.offsetParent as HTMLElement;
    }

    return { xCoord, yCoord };
  }

  function addOscillatorModule(moduleId: string): Module {
    return {
      moduleId,
      moduleType: ModuleType.__OSCILLATOR,
      inPorts: {
        [OscillatorInPortType.__FREQ_MOD]: { cableId: null },
        [OscillatorInPortType.__PUL_WIDTH_MOD]: { cableId: null },
        [OscillatorInPortType.__VOLT_PER_OCT]: { cableId: null },
        [OscillatorInPortType.__SYNC]: { cableId: null },
      },
      outPorts: {
        [OscillatorOutPortType.__SIN]: { cableIds: [] },
        [OscillatorOutPortType.__TRI]: { cableIds: [] },
        [OscillatorOutPortType.__SAW]: { cableIds: [] },
        [OscillatorOutPortType.__SQR]: { cableIds: [] },
        [OscillatorOutPortType.__PUL]: { cableIds: [] },
      },
      handleId: addHandle(),
    };
  }

  function addModule(moduleType: ModuleType): string {
    let moduleId: string;
    do {
      moduleId = uuid();
    } while (moduleId in modules);

    modules[moduleId] = {
      [ModuleType.__TO_DEVICE]: addOscillatorModule,
      [ModuleType.__FROM_DEVICE]: addOscillatorModule,
      [ModuleType.__OSCILLATOR]: addOscillatorModule,
      [ModuleType.__ENVELOPE]: addOscillatorModule,
      [ModuleType.__FILTER]: addOscillatorModule,
      [ModuleType.__AMPLIFIER]: addOscillatorModule,
      [ModuleType.__MIXER]: addOscillatorModule,
    }[moduleType](moduleId);

    return moduleId;
  }

  function removeModule(moduleId: string): void {
    const module = modules[moduleId];

    for (const inPort of Object.values(module.inPorts)) {
      removeCable(inPort.cableId);
    }

    for (const outPort of Object.values(module.outPorts)) {
      for (const cableId of outPort.cableIds) {
        removeCable(cableId);
      }
    }

    removeHandle(module.handleId);

    delete modules[moduleId];
  }

  function addCable(): string {
    let cableId: string;
    do {
      cableId = uuid();
    } while (cableId in cables);

    cables[cableId] = {
      cableId,
      inPlug: {
        moduleId: null,
        inPortId: null,
        handleId: addHandle(),
      },
      outPlug: {
        moduleId: null,
        outPortId: null,
        handleId: addHandle(),
      },
      zCoord: 0,
      color: [
        "hsl(40 90% 70%)",
        "hsl(0 90% 70%)",
        "hsl(120, 90%, 70%)",
        "hsl(220, 90%, 70%)",
        "hsl(300, 90%, 70%)",
      ][Math.floor(Math.random() * 5)],
    };

    return cableId;
  }

  function removeCable(cableId: string): void {
    const cable = cables[cableId];

    if (cable.inPlug.moduleId && cable.inPlug.inPortId) {
      disconnectInPlugFromInPort(cableId);
    }

    if (cable.outPlug.moduleId && cable.outPlug.outPortId) {
      disconnectOutPlugFromOutPort(cableId);
    }

    removeHandle(cable.inPlug.handleId);
    removeHandle(cable.outPlug.handleId);

    delete cables[cableId];
  }

  function connectInPlugToInPort(cableId: string, moduleId: string, inPortId: string): void {
    const cable = cables[cableId];
    const module = modules[moduleId];

    module.inPorts[inPortId].cableId = cableId;

    cable.inPlug.moduleId = moduleId;
    cable.inPlug.inPortId = inPortId;
  }

  function disconnectInPlugFromInPort(cableId: string): void {
    const cable = cables[cableId];
    const module = modules[cable.inPlug.moduleId];

    module.inPorts[cable.inPlug.inPortId].cableId = null;

    cable.inPlug.moduleId = null;
    cable.inPlug.inPortId = null;
  }

  function connectOutPlugToOutPort(cableId: string, moduleId: string, outPortId: string): void {
    const cable = cables[cableId];
    const module = modules[moduleId];

    module.outPorts[outPortId].cableIds.push(cableId);

    cable.outPlug.moduleId = moduleId;
    cable.outPlug.outPortId = outPortId;
  }

  function disconnectOutPlugFromOutPort(cableId: string): void {
    const cable = cables[cableId];
    const module = modules[cable.outPlug.moduleId];

    module.outPorts[cable.outPlug.outPortId].cableIds = module.outPorts[
      cable.outPlug.outPortId
    ].cableIds.filter((cableId: string): boolean => cableId !== cable.cableId);

    cable.outPlug.moduleId = null;
    cable.outPlug.outPortId = null;
  }

  function addHandle(handleId: string): void {
    handles[handleId] = {
      handleId,
      xCoord: 0,
      yCoord: 0,
    };
  }

  function removeHandle(handleId: string): void {
    delete handles[handleId];
  }

  function moveHandle(handleId: string, xCoord: number, yCoord: number): void {
    const handle = handles[handleId];

    const deltaXCoord = xCoord - handle.xCoord;
    const deltaYCoord = yCoord - handle.yCoord;

    handle.xCoord = xCoord;
    handle.yCoord = yCoord;

    for (const child of handle.children) {
      moveHandle(child, handles[child].xCoord + deltaXCoord, handles[child].yCoord + deltaYCoord);
    }
  }

  function selectHandle(handleId: string) {
    const handle = handles[mouse.handleId];
    handle.children.push(handleId);
  }

  function deselectHandle(handleId: string) {
    const handle = handles[mouse.handleId];
    handle.children = handle.children.filter((child) => child !== handleId);
  }

  setContext("addHandle", {
    calcCoords,
    addModule,
    removeModule,
    addCable,
    removeCable,
    connectInPlugToInPort,
    disconnectInPlugFromInPort,
    connectOutPlugToOutPort,
    disconnectOutPlugFromOutPort,
    updateTransform,
    selectTransform,
    deselectTransform
  });
  // module::4741f751-6220-46a1-91b5-da0727d8375d
  // cable::4741f751-6220-46a1-91b5-da0727d8375d::in-plug
  // cable::4741f751-6220-46a1-91b5-da0727d8375d::out-plug


  function addTransform() {

  }

  function removeTransform() {

  }

  function updateTransform() {

  }

  function selectTransform() {

  }
  
  function deselectTransform() {

  }

  // idea: there's a border around the rack where if you drop modules there, they are deleted

  // JS
  // modules, inPlugs, outPlugs
  // use $derived rune to keep a reference to floating plugs/module (any inPlugs without inPorts, outPlugs without outPorts)
  // 
  // calcCoords(element: HTMLElement),

  // addModule(moduleType: ModuleType),
  // removeModule(moduleId: string),
  // addCable,
  // removeCable,
  // connectInPlugToInPort,
  // disconnectInPlugFromInPort,
  // connectOutPlugToOutPort,
  // disconnectOutPlugFromOutPort,
  // 
  //
  // Separate handles object that references modules/cables via URN. This is the fake polymorphism part.
  // This also decouples entities from drawing logic.
  // addHandle(handleId: string)
  // removeHandle()
  // moveHandle()
  // selectHandle()
  // deselectHandle()
  //
  // handles have Trans?
  //
  // what the fuck is this abstraction hell


  // JS
  // module -> inPort -> inPlug <-> outPlug <- outPort <- module
  //                     (     cable      )
  // C++
  // module -> inPort <----------------------> outPort <- module  (storing outPortId in inPort also tells you whether this port is connected or not)






  // alt, keeping a list of handle to move is easy
  (xOffset: number, yOffset: number, isValid: boolean) => {
    moveHandle(module.handleId, xOffset, yOffset);

    for (const inPort of Object.values(module.inPorts)) {
      const cable = cables[inPort.cableId];
      moveHandle(cable.inPlug.handleId, xOffset, yOffset);
    }

    for (const outPort of Object.values(module.outPorts)) {
      for (const cableId of outPort.cableIds) {
        const cable = cables[cableId];
        moveHandle(cable.outPlug.handleId, xOffset, yOffset);
      }
    }
  };

  () => {
    for (const module of Object.values(modules)) {
      const handle = handles[module.handleId];
      moveHandle(
        module.handleId,
        Math.max(0, Math.round(handle.xCoord / unit.width) * unit.width),
        Math.max(0, Math.round(handle.yCoord / unit.height) * unit.height),
      );
    }

    const sorted = Object.values(modules).sort((firstModule, secondModule) => {
      const firstHandle = handles[firstModule.handleId];
      const secondHandle = handles[secondModule.handleId];

      return firstHandle.yCoord - secondHandle.yCoord || firstHandle.xCoord - secondHandle.xCoord;
    });

    let xCoord = 0;
    let yCoord = 0;
    for (const module of sorted) {
      const handle = handles[module.handleId];

      if (handle.yCoord !== yCoord) {
        xCoord = handle.xCoord;
        yCoord = handle.yCoord;
      }

      if (handle.xCoord < xCoord) {
        moveHandle(module.handleId, xCoord, handle.yCoord);
      }
      xCoord = handle.xCoord + dimensions[module.moduleType].width;
    }

    for (const [cableId, cable] of Object.entries(cables)) {
      if (!cable.inPlug.moduleId && !cable.inPlug.inPortId) {
        removeCable(cableId);
      }

      if (!cable.outPlug.moduleId && !cable.outPlug.outPortId) {
        removeCable(cableId);
      }
    }
  };

  // if moved on top of port and deselected -> connect
  // else -> disconnect

  // PRINCIPLE: things are based on the position and selected/deselected status of PLUGS
  // PRINCIPLE: only ONE thing is selected at a given time (plug or module)
  // therefore, fire a "update state" callback on mouse move, down, up
  // but ONLY check components that might change -> register/deregister components as necessary
  // handles are things that are movable

  // a big headache was that I didn't want enums to track whether the selected object was a module or cable
  // at the time of onmousedown, you could attach global callbacks to play onmousemove and onmousedown
  // could attach state entirely within these callbacks?

  // register callbacks in array and call each

  function handleMouseMove(event: MouseEvent): void {
    if (!onMouseMove) return;
    // moveHandle(mouse.handleId, event.clientX, event.clientY);
    onMouseMove(event.clientX, event.clientY);
  }

  function handleMouseUp(event: MouseEvent): void {
    if (!onMouseUp) return;
    onMouseUp(event.clientX, event.clientY);
    onMouseUp = null;
  }
</script>

<div class="rack-outer">
  <!-- svelte-ignore a11y_no_static_element_interactions -->
  <div
    class="rack-inner"
    onmousemove={handleMouseMove}
    onmouseup={handleMouseUp}
    bind:this={rackElement}
  >
    {#each Object.values(modules) as module}
      {@const Module = Modules[module.moduleType]}
      <Module {module} {cables} />
    {/each}

    {#each Object.values(cables) as cable}
      <Cable {cable} />
    {/each}
  </div>
  <div class="rack-widget">
    <button
      onclick={() => {
        addModule(ModuleType.__TO_DEVICE);
      }}
    >
      TO DEVICE
    </button>
    <button
      onclick={() => {
        addModule(ModuleType.__OSCILLATOR);
      }}
    >
      VCO
    </button>
    <button
      onclick={() => {
        addModule(ModuleType.__FILTER);
      }}
    >
      VCF
    </button>
  </div>
</div>

<style>
  .rack-outer {
  }
  .rack-inner {
    position: relative;
    width: 100vw;
    min-height: 100vh;
  }
  .rack-widget {
    position: fixed;
    bottom: 50px;
    right: 50px;
  }
</style>
