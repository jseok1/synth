<script lang="ts">
  import { getContext } from "svelte";

  let { module, children } = $props();

  const { dragModule } = getContext("context.api");

  function handleMouseDown(event: MouseEvent): void {
    dragModule(module.moduleId, module.xCoord, module.yCoord, false);
  }
</script>

<!-- svelte-ignore a11y_no_static_element_interactions -->
<div
  class={["module", "module-outer", !module.isDropped && "is-dragging"]}
  style:top={`${module.yCoord}px`}
  style:left={`${module.xCoord}px`}
  style:height={`${module.height}px`}
  style:width={`${module.width}px`}
  onmousedown={handleMouseDown}
>
  <div class="module-inner">
    <div class="module-type">VCO</div>
    {#if children}
      {@render children()}
    {/if}
  </div>
</div>

<style>
  .module {
    background-color: var(--color-light-grey);
    border: 2px solid var(--color-medium-grey);
    padding: 10px;
  }

  .module.is-dragging {
    opacity: 0.75;
  }

  .module-outer {
    position: absolute;
  }
  .module-inner {
    position: relative;
  }

  .module .module-type {
    width: 100%;
    padding: 0 0 10px;
    text-align: center;
    font-weight: bold;
  }
</style>
