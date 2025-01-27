<script lang="ts">
  let {
    label,
    min,
    max,
    value = $bindable(),
  }: {
    label: string;
    min: number;
    max: number;
    value: number;
  } = $props();

  function handleMouseDown(event) {
    event.stopPropagation();
  }
</script>

<!-- svelte-ignore a11y_no_static_element_interactions -->
<div class="slider" onmousedown={handleMouseDown}>
  <input type="range" id="freq" name="freq" {min} {max} step={0.01} bind:value />
  <label for="freq">{label}</label>
</div>

<style>
  .slider {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-self: center;
  }
  .slider label {
    font-size: var(--font-size-xs);
  }
  input[type="range"] {
    -webkit-appearance: none;
    appearance: none;
    background: transparent;
    cursor: pointer;
    width: 100%;
  }
  input[type="range"]::-webkit-slider-runnable-track {
    background: var(--color-black);
    height: var(--slider-track-height);
    border-radius: 5px;
    margin: 10px 0;
  }
  input[type="range"]::-webkit-slider-thumb {
    -webkit-appearance: none;
    appearance: none;
    margin-top: calc((var(--slider-track-height) - var(--slider-thumb-height)) / 2);
    background-color: var(--color-light-grey);
    height: var(--slider-thumb-height);
    width: 20px;
    border-radius: 5px;
    border: 1.5px solid var(--color-black);
  }
  input[type="range"]:focus {
    outline: none;
  }
  input[type="range"]:focus::-webkit-slider-thumb {
    outline: none;
  }
</style>
