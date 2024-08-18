#include "OutRackModule.hpp"

// somehow enfore singleton?
OutRackModule::OutRackModule(double freq_sample)
  : Module{
      freq_sample,
      std::unordered_map<int, double>{},
      std::unordered_map<int, InPort>{{OutRackModuleInPort::in_t, InPort{0.0, false}}},
      std::unordered_map<int, OutPort>{}
    } {}

void OutRackModule::process() {}
