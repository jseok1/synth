#ifndef MIXER_MODULE_HPP
#define MIXER_MODULE_HPP

#include <AbstractModule.hpp>
#include <array>

class MixerModule : public AbstractModule {
 public:
  enum MixerParam {
  };
  enum MixerInPort {
    in_1_t,
    in_2_t
  };
  enum MixerOutPort {
    out_t
  };

  std::array<double, 0> params;
  std::array<double, 2> in_ports;
  std::array<double, 1> out_ports;

  MixerModule(double freq_sample) ;
  void process() override;
};

#endif
