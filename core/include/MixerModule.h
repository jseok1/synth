#ifndef MIXER_MODULE_H
#define MIXER_MODULE_H

#include <unordered_map>

#include "Module.h"

class MixerModule : public Module {
 public:
  enum MixerParam : int {
    amp_mod_amt_1_t,
    amp_mod_amt_2_t,
    amp_mod_amt_3_t,
    amp_mod_amt_4_t
  };
  enum MixerInPort : int {
    in_1_t,
    in_2_t,
    in_3_t,
    in_4_t
  };
  enum MixerOutPort : int {
    out_t
  };

  MixerModule(double freq_sample);

  void process() override;
};

#endif
