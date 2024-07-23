#ifndef OSCILLATOR_MODULE_HPP
#define OSCILLATOR_MODULE_HPP

#include <Module.hpp>
#include <unordered_map>

class OscillatorModule : public Module {
 public:
  enum class OscillatorParam {
    freq_t,
    freq_mod_amt_t,
    pul_width_t,
    pul_width_mod_amt_t
  };
  enum class OscillatorInPort {
    freq_mod_t,
    pul_width_mod_t,
    volt_per_oct_t,
    sync_t
  };
  enum class OscillatorOutPort {
    sin_t,
    tri_t,
    saw_t,
    sqr_t,
    pul_t
  };

  std::unordered_map<OscillatorParam, double> params;
  std::unordered_map<OscillatorInPort, double> in_ports;
  std::unordered_map<OscillatorOutPort, double> out_ports;

  OscillatorModule(double freq_sample);
  
  void process() override;

 private:
  double phase_tm1;
  double sync_tm1;

  static double sin(double phase_t);
  static double tri(double phase_t);
  static double saw(double phase_t);
  static double sqr(double phase_t);
  static double pul(double phase_t, double pul_width_t);
};

#endif
