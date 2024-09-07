#include "modules/Module.hpp"

Module::Module(
  double freq_sample,
  std::unordered_map<int, double> params,
  std::unordered_map<int, InPort> in_ports,
  std::unordered_map<int, OutPort> out_ports
)
  : freq_sample{freq_sample},
    params{params},
    in_ports{in_ports},
    out_ports{out_ports} {}

Module::~Module() {}
