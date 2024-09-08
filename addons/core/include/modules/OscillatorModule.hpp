#ifndef OSCILLATOR_MODULE_HPP
#define OSCILLATOR_MODULE_HPP

#include <unordered_map>

#include "modules/Module.hpp"

class OscillatorModule : public Module {
 public:
  enum OscillatorParam : int {
    __FREQ,
    __FREQ_MOD_AMT,
    __PUL_WIDTH,
    __PUL_WIDTH_MOD_AMT
  };
  enum OscillatorInPort : int {
    __FREQ_MOD,
    __PUL_WIDTH_MOD,
    __VOLT_PER_OCT,
    __SYNC
  };
  enum OscillatorOutPort : int {
    __SIN,
    __TRI,
    __SAW,
    __SQR,
    __PUL
  };

  OscillatorModule(double freq_sample);

  void process() override;

 private:
  double phase_tm1;
  double sync_tm1;
  double freq_tm1; // TODO: remove

  static double sin(double phase_t);
  static double tri(double phase_t);
  static double saw(double phase_t);
  static double sqr(double phase_t);
  static double pul(double phase_t, double pul_width_t);
};

#endif
