#ifndef AMPLIFIER_MODULE_H
#define AMPLIFIER_MODULE_H

#include <unordered_map>

#include "Module.h"

class AmplifierModule : public Module {
 public:
  enum AmplifierParam : int {
    amp_mod_amt_t
  };
  enum AmplifierInPort : int {
    amp_mod_t,
    in_t
  };
  enum AmplifierOutPort : int {
    out_t
  };

  AmplifierModule(double freq_sample);

  void process() override;
};

#endif
