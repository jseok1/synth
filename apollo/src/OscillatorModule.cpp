#include <OscillatorModule.hpp>
#include <algorithm>
#include <cmath>

OscillatorModule::OscillatorModule(double freq_sample)
  : AbstractModule{freq_sample},
    params{
      {OscillatorParam::freq_t, 0},
      {OscillatorParam::freq_mod_amt_t, 0},
      {OscillatorParam::pul_width_t, 0},
      {OscillatorParam::pul_width_mod_amt_t, 0}
    },
    in_ports{
      {OscillatorInPort::freq_mod_t, 0},
      {OscillatorInPort::pul_width_mod_t, 0},
      {OscillatorInPort::volt_per_oct_t, 0},
      {OscillatorInPort::sync_t, 0}
    },
    out_ports{
      {OscillatorOutPort::sin_t, 0},
      {OscillatorOutPort::tri_t, 0},
      {OscillatorOutPort::saw_t, 0},
      {OscillatorOutPort::sqr_t, 0},
      {OscillatorOutPort::pul_t, 0}
    },
    phase_tm1{0},
    sync_tm1{0} {}

void OscillatorModule::process() {
  auto freq_t = params[OscillatorParam::freq_t];
  auto freq_mod_amt_t = params[OscillatorParam::freq_mod_amt_t];
  auto pul_width_t = params[OscillatorParam::pul_width_t];
  auto pul_width_mod_amt_t = params[OscillatorParam::pul_width_mod_amt_t];

  auto freq_mod_t = in_ports[OscillatorInPort::freq_mod_t];
  auto pul_width_mod_t = in_ports[OscillatorInPort::pul_width_mod_t];
  auto volt_per_oct_t = in_ports[OscillatorInPort::volt_per_oct_t];
  auto sync_t = in_ports[OscillatorInPort::sync_t];

  auto &sin_t = out_ports[OscillatorOutPort::sin_t];
  auto &tri_t = out_ports[OscillatorOutPort::tri_t];
  auto &saw_t = out_ports[OscillatorOutPort::saw_t];
  auto &sqr_t = out_ports[OscillatorOutPort::sqr_t];
  auto &pul_t = out_ports[OscillatorOutPort::pul_t];

  freq_t *= std::pow(2, volt_per_oct_t / 12) * (1 + freq_mod_t * freq_mod_amt_t);
  pul_width_t *= 1 + pul_width_mod_t * pul_width_mod_amt_t;

  freq_t = std::clamp(freq_t, 8.176, 12543.855);
  pul_width_t = std::clamp(pul_width_t, 0.01, 0.99);

  double phase_t = std::fmod(phase_tm1 + freq_t / freq_sample, 1);

  if (sync_tm1 < 0 && sync_t >= 0) {
    phase_t = 0;
  }

  sin_t = sin(phase_t);
  tri_t = tri(phase_t);
  saw_t = saw(phase_t);
  sqr_t = sqr(phase_t);
  pul_t = pul(phase_t, pul_width_t);

  phase_tm1 = phase_t;
  sync_tm1 = sync_t;
}

double OscillatorModule::sin(double phase_t) {
  return std::sin(2 * M_PI * phase_t);
}

double OscillatorModule::tri(double phase_t) {
  phase_t = std::fmod(phase_t, 1);
  return phase_t < 0.25 ? 4 * phase_t
                        : (phase_t < 0.75 ? 2 - 4 * phase_t : 4 * phase_t - 4);
}

double OscillatorModule::saw(double phase_t) {
  phase_t = std::fmod(phase_t, 1);
  return 2 * phase_t - 1;
}

double OscillatorModule::sqr(double phase_t) {
  phase_t = std::fmod(phase_t, 1);
  return phase_t < 0.5 ? 1 : -1;
}

double OscillatorModule::pul(double phase_t, double pul_width_t) {
  phase_t = std::fmod(phase_t, 1);
  return phase_t < pul_width_t ? 1 : -1;
}
