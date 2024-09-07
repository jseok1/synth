#include "modules/ToDeviceModule.hpp"

// TODO: enfore singleton
ToDeviceModule::ToDeviceModule(double freq_sample)
  : Module{
      freq_sample,
      std::unordered_map<int, double>{},
      std::unordered_map<int, InPort>{{ToDeviceInPort::in_t, InPort{0.0, false}}},
      std::unordered_map<int, OutPort>{}
    } {}

void ToDeviceModule::process() {}
