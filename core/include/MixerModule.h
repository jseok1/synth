#ifndef MIXER_MODULE_H
#define MIXER_MODULE_H

#include <unordered_map>

#include "Module.h"

class MixerModule : public Module {
 public:
  enum class MixerParam {
    amp_mod_amt_1_t,
    amp_mod_amt_2_t,
    amp_mod_amt_3_t,
    amp_mod_amt_4_t
  };
  enum class MixerInPort {
    in_1_t,
    in_2_t,
    in_3_t,
    in_4_t
  };
  enum class MixerOutPort {
    out_t
  };

  std::unordered_map<MixerParam, double> params;
  std::unordered_map<MixerInPort, double> in_ports;
  std::unordered_map<MixerOutPort, double> out_ports;

  MixerModule(double freq_sample);

  void process() override;
};

#endif
