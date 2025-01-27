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
  xCoord: number;
  yCoord: number;
  isDropped: boolean;
}

interface InPlug {
  moduleId: string | null;
  inPortId: string | null;
  xCoord: number;
  yCoord: number;
  isDropped: boolean;
}

interface OutPlug {
  moduleId: string | null;
  outPortId: string | null;
  xCoord: number;
  yCoord: number;
  isDropped: boolean;
}

interface Cable {
  cableId: string;
  inPlug: InPlug;
  outPlug: OutPlug;
  zCoord: number;
  color: string; // better type for this? maybe use a color enum of possible values
}

interface Rack {
  modules: {
    [moduleId: string]: Module;
  };
  cables: {
    [cableId: string]: Cable;
  };
}
