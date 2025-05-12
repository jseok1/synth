enum ModuleType {
  __TO_DEVICE,
  __FROM_DEVICE,
  __OSCILLATOR,
  __ENVELOPE,
  __FILTER,
  __AMPLIFIER,
  __MIXER,
}

enum OscillatorParamType {
  __FREQ,
  __FREQ_MOD_AMT,
  __PUL_WIDTH,
  __PUL_WIDTH_MOD_AMT,
}

enum OscillatorInPortType {
  __FREQ_MOD,
  __PUL_WIDTH_MOD,
  __VOLT_PER_OCT,
  __SYNC,
}

enum OscillatorOutPortType {
  __SIN,
  __TRI,
  __SAW,
  __SQR,
  __PUL,
}

interface Transform {
  xCoord: number;
  yCoord: number;
}

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
  transform: Transform;
}

interface InPlug {
  moduleId: string;
  inPortId: string;
  transform: Transform;
}

interface OutPlug {
  moduleId: string;
  outPortId: string;
  transform: Transform;
}

interface Cable {
  cableId: string;
  inPlug: InPlug;
  outPlug: OutPlug;
  zCoord: number;
}

interface Modules {
  [moduleId: string]: Module;
}

interface Cables {
  [cableId: string]: Cable;
}

interface Rack {
  modules: Modules;
  cables: Cables;
  selected: { transformId: string };
}
