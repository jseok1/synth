<script lang="ts">
  import Module from "./Module.svelte";
  import InPort from "../InPort.svelte";
  import OutPort from "../OutPort.svelte";
  import Knob from "../Knob.svelte";
  import { getContext } from "svelte";

  let { module, cables } = $props();

  const params = $state({
    [OscillatorParamType.__FREQ]: 8.175799 * Math.pow(2, 3),
    [OscillatorParamType.__FREQ_MOD_AMT]: 0.0,
    [OscillatorParamType.__PUL_WIDTH]: 0.5,
    [OscillatorParamType.__PUL_WIDTH_MOD_AMT]: 0.0,
  });
</script>

<Module {module}>
  <Knob label="FREQ" min={0} max={1000} bind:value={params[OscillatorParamType.__FREQ]} />
  <div>{params[OscillatorParamType.__FREQ]}</div>

  <div class="ports">
    <InPort {module} inPortId={OscillatorInPortType.__FREQ_MOD} label="FM" {cables} />
    <InPort {module} inPortId={OscillatorInPortType.__PUL_WIDTH_MOD} label="PWM" {cables} />
    <InPort {module} inPortId={OscillatorInPortType.__VOLT_PER_OCT} label="V/OCT" {cables} />
    <InPort {module} inPortId={OscillatorInPortType.__SYNC} label="SYNC" {cables} />
  </div>
  <div class="ports">
    <OutPort {module} outPortId={OscillatorOutPortType.__SIN} label="SIN" {cables} />
    <OutPort {module} outPortId={OscillatorOutPortType.__TRI} label="TRI" {cables} />
    <OutPort {module} outPortId={OscillatorOutPortType.__SAW} label="SAW" {cables} />
    <OutPort {module} outPortId={OscillatorOutPortType.__SQR} label="SQR" {cables} />
  </div>
</Module>

<style>
  .ports {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
  }
</style>
