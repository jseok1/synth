<script lang="ts">
  import { setContext } from "svelte";
  import Cable from "./Cable.svelte";
  import OscillatorModule, { addOscillatorModule } from "./modules/OscillatorModule.svelte";

  import { v4 as uuid } from "uuid";
  import Module from "./modules/Module.svelte";

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

  const { modules, cables } = $state<Rack>({ modules: {}, cables: {} });
  const cursorCoords = { xCoord: 0, yCoord: 0 };

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

  function addModule(moduleType: ModuleType): string {
    let moduleId: string;
    do {
      moduleId = uuid();
    } while (moduleId in modules);

    modules[moduleId] = {
      [ModuleType.__TO_DEVICE]: addOscillatorModule(moduleId),
      [ModuleType.__FROM_DEVICE]: addOscillatorModule(moduleId),
      [ModuleType.__OSCILLATOR]: addOscillatorModule(moduleId),
      [ModuleType.__ENVELOPE]: addOscillatorModule(moduleId),
      [ModuleType.__FILTER]: addOscillatorModule(moduleId),
      [ModuleType.__AMPLIFIER]: addOscillatorModule(moduleId),
      [ModuleType.__MIXER]: addOscillatorModule(moduleId),
    }[moduleType];

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

    delete modules[moduleId];
  }

  function dragModule(moduleId: string, xCoord: number, yCoord: number, drop: boolean): void {
    const module = modules[moduleId];

    const xOffset = xCoord - module.xCoord;
    const yOffset = yCoord - module.yCoord;

    module.xCoord = xCoord;
    module.yCoord = yCoord;
    module.isDropped = drop;

    for (const inPort of Object.values(module.inPorts)) {
      if (inPort.cableId) {
        const cable = cables[inPort.cableId];
        dragInPlug(
          inPort.cableId,
          cable.inPlug.xCoord + xOffset,
          cable.inPlug.yCoord + yOffset,
          drop,
        );
      }
    }

    for (const outPort of Object.values(module.outPorts)) {
      for (const cableId of outPort.cableIds) {
        const cable = cables[cableId];
        dragOutPlug(cableId, cable.outPlug.xCoord + xOffset, cable.outPlug.yCoord + yOffset, drop);
      }
    }
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
        xCoord: 0,
        yCoord: 0,
        isDropped: true,
      },
      outPlug: {
        moduleId: null,
        outPortId: null,
        xCoord: 0,
        yCoord: 0,
        isDropped: true,
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

    delete cables[cableId];
  }

  function dragInPlug(cableId: string, xCoord: number, yCoord: number, drop: boolean): void {
    const cable = cables[cableId];

    cable.inPlug.xCoord = xCoord;
    cable.inPlug.yCoord = yCoord;
    cable.inPlug.isDropped = drop;
  }

  function dragOutPlug(cableId: string, xCoord: number, yCoord: number, drop: boolean): void {
    const cable = cables[cableId];

    cable.outPlug.xCoord = xCoord;
    cable.outPlug.yCoord = yCoord;
    cable.outPlug.isDropped = drop;
  }

  function connectInPlugToInPort(cableId: string, moduleId: string, inPortId: string): void {
    const cable = cables[cableId];

    const inPort = modules[moduleId].inPorts[inPortId];
    inPort.cableId = cableId;

    cable.inPlug.moduleId = moduleId;
    cable.inPlug.inPortId = inPortId;
  }

  function disconnectInPlugFromInPort(cableId: string): void {
    const cable = cables[cableId];

    const inPort = modules[cable.inPlug.moduleId].inPorts[cable.inPlug.inPortId];
    inPort.cableId = null;

    cable.inPlug.moduleId = null;
    cable.inPlug.inPortId = null;
  }

  function connectOutPlugToOutPort(cableId: string, moduleId: string, outPortId: string): void {
    const cable = cables[cableId];

    const outPort = modules[moduleId].outPorts[outPortId];
    outPort.cableIds.push(cableId);

    cable.outPlug.moduleId = moduleId;
    cable.outPlug.outPortId = outPortId;
  }

  function disconnectOutPlugFromOutPort(cableId: string): void {
    const cable = cables[cableId];

    const outPort = modules[cable.outPlug.moduleId].outPorts[cable.outPlug.outPortId];
    outPort.cableIds = outPort.cableIds.filter(
      (cableId: string): boolean => cableId !== cable.cableId, // cable.cableId
    );

    cable.outPlug.moduleId = null;
    cable.outPlug.outPortId = null;
  }

  setContext("rack", {
    calcCoords,
    addModule,
    removeModule,
    dragModule,
    addCable,
    removeCable,
    dragInPlug,
    dragOutPlug,
    connectInPlugToInPort,
    disconnectInPlugFromInPort,
    connectOutPlugToOutPort,
    disconnectOutPlugFromOutPort,
  });

  function handleMouseMove(event: MouseEvent): void {
    const xOffset = event.clientX - cursorCoords.xCoord;
    const yOffset = event.clientY - cursorCoords.yCoord;

    cursorCoords.xCoord = event.clientX;
    cursorCoords.yCoord = event.clientY;

    for (const [moduleId, module] of Object.entries(modules)) {
      if (!module.isDropped) {
        dragModule(moduleId, module.xCoord + xOffset, module.yCoord + yOffset, false);
        return; // idk about this
      }
    }

    for (const [cableId, cable] of Object.entries(cables)) {
      if (!cable.inPlug.isDropped) {
        dragInPlug(cableId, cable.inPlug.xCoord + xOffset, cable.inPlug.yCoord + yOffset, false);
      }

      if (!cable.outPlug.isDropped) {
        dragOutPlug(cableId, cable.outPlug.xCoord + xOffset, cable.outPlug.yCoord + yOffset, false);
      }
    }
  }

  function handleMouseUp(event: MouseEvent): void {
    for (const [moduleId, module] of Object.entries(modules)) {
      if (!module.isDropped) {
        dragModule(
          moduleId,
          Math.max(0, Math.round(module.xCoord / unit.width) * unit.width),
          Math.max(0, Math.round(module.yCoord / unit.height) * unit.height),
          true,
        );
      }
    }

    const yCoords = Object.groupBy(
      Object.values(modules),
      (module: Module): number => module.yCoord,
    );
    for (const group of Object.values(yCoords)) {
      group.sort((thisModule, thatModule) => thisModule.xCoord - thatModule.xCoord);
      // is there a different algo?

      let xCoord = 0;
      for (const module of group) {
        if (module.xCoord < xCoord) {
          dragModule(module.moduleId, xCoord, module.yCoord, true);
        }
        xCoord = module.xCoord + module.width;
      }
    }

    for (const [cableId, cable] of Object.entries(cables)) {
      if (!cable.inPlug.isDropped) {
        removeCable(cableId);
      }

      if (!cable.outPlug.isDropped) {
        removeCable(cableId);
      }
    }
  }
</script>

<!-- 
    calcCoords,
    addModule,
    removeModule,
    addCable,
    removeCable,
    connectInPlugToInPort,
    disconnectInPlugFromInPort,
    connectOutPlugToOutPort,
    disconnectOutPlugFromOutPort,
    moveHandle,
    selectHandle,
    deselectHandle

{ selected, modules, cables }


interface InPort {
  cableId: string | null;
}

interface OutPort {
  cableIds: string[];
}

interface Module {
  moduleId: string;
  moduleType: ModuleType;
  inPorts: {
    [inPortId: string]: InPort;
  };
  outPorts: {
    [outPortId: string]: OutPort;
  };
  handleId: string;
}
^ technically ports aren't necessary unless you want to change state in the module based on connectedness
(which maybe?)

interface InPlug {
  moduleId: string | null;
  inPortId: string | null;
  handleId: string;
}

interface OutPlug {
  moduleId: string | null;
  outPortId: string | null;
  handleId: string;
}

interface Cable {
  cableId: string;
  inPlug: InPlug;
  outPlug: OutPlug;
  zCoord: number;
  color: string;
}

/** this decouples state vs position */
interface Handle {
  handleId: string;
  xCoord: number;
  yCoord: number;
  dependencies: number[];
}


-->

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
