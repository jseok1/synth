#ifndef MIXER_MODULE_HPP
#define MIXER_MODULE_HPP

#include <unordered_map>

#include "modules/Module.hpp"

class MixerModule : public Module {
 public:
  enum MixerParam : int {
    __AMP_MOD_AMT_1,
    __AMP_MOD_AMT_2,
    __AMP_MOD_AMT_3,
    __AMP_MOD_AMT_4
  };
  enum MixerInPort : int {
    __IN_1,
    __IN_2,
    __IN_3,
    __IN_4
  };
  enum MixerOutPort : int {
    __OUT
  };

  MixerModule(double freq_sample);

  void process() override;
};

#endif
