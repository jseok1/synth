#ifndef AMPLIFIER_MODULE_H
#define AMPLIFIER_MODULE_H

#include <unordered_map>

#include "Module.h"

class AmplifierModule : public Module {
 public:
  enum class AmplifierParam {
    amp_mod_amt_t
  };
  enum class AmplifierInPort {
    amp_mod_t,
    in_t
  };
  enum class AmplifierOutPort {
    out_t
  };

  std::unordered_map<AmplifierParam, double> params;
  std::unordered_map<AmplifierInPort, double> in_ports;
  std::unordered_map<AmplifierOutPort, double> out_ports;

  AmplifierModule(double freq_sample);

  void process() override;
};

#endif
