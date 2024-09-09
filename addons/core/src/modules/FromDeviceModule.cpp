#include "modules/FromDeviceModule.hpp"

// TODO: enfore singleton
FromDeviceModule::FromDeviceModule(double freq_sample)
  : Module{
      freq_sample,
      std::unordered_map<int, double>{},
      std::unordered_map<int, InPort>{},
      std::unordered_map<int, OutPort>{}
    } {}

void FromDeviceModule::process() {}
