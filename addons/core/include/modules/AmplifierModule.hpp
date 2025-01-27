#ifndef AMPLIFIER_MODULE_HPP
#define AMPLIFIER_MODULE_HPP

#include <unordered_map>

#include "modules/Module.hpp"

class AmplifierModule : public Module {
 public:
  enum AmplifierParam : int {
    __AMP_MOD_AMT
  };
  enum AmplifierInPort : int {
    __AMP_MOD,
    __IN
  };
  enum AmplifierOutPort : int {
    __OUT
  };

  AmplifierModule(double freq_sample);

  void process() override;
};

#endif
