#ifndef OSCILLATOR_MODULE_HPP
#define OSCILLATOR_MODULE_HPP

#include <unordered_map>

#include "modules/Module.hpp"

class OscillatorModule : public Module {
 public:
  enum OscillatorParam : int {
    freq_t,
    freq_mod_amt_t,
    pul_width_t,
    pul_width_mod_amt_t
  };
  enum OscillatorInPort : int {
    freq_mod_t,
    pul_width_mod_t,
    volt_per_oct_t,
    sync_t
  };
  enum OscillatorOutPort : int {
    sin_t,
    tri_t,
    saw_t,
    sqr_t,
    pul_t
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
