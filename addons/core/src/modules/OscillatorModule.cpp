#include "modules/OscillatorModule.hpp"

#include <algorithm>
#include <cmath>
#include <iostream>
#include <chrono>

OscillatorModule::OscillatorModule(double freq_sample)
  : Module{freq_sample, {
      {OscillatorParam::__FREQ, 8.175799 * std::pow(2, 2)},  // 32': 2, 16': 3, 8': 4, 4': 5, 2': 6
      {OscillatorParam::__FREQ_MOD_AMT, 0.0},
      {OscillatorParam::__PUL_WIDTH, 0.5},
      {OscillatorParam::__PUL_WIDTH_MOD_AMT, 0.0}
    }, {
      {OscillatorInPort::__FREQ_MOD, InPort{0.0, false}},
      {OscillatorInPort::__PUL_WIDTH_MOD, InPort{0.0, false}},
      {OscillatorInPort::__VOLT_PER_OCT, InPort{0.0, false}},
      {OscillatorInPort::__SYNC, InPort{0.0, false}}
    }, {
      {OscillatorOutPort::__SIN, OutPort{0.0}},
      {OscillatorOutPort::__TRI, OutPort{0.0}},
      {OscillatorOutPort::__SAW, OutPort{0.0}},
      {OscillatorOutPort::__SQR, OutPort{0.0}},
      {OscillatorOutPort::__PUL, OutPort{0.0}}
    }},
    phase_tm1{0.0},
    sync_tm1{0.0},
    freq_tm1{0.0} {}

void OscillatorModule::process() {
  auto freq_t = params[OscillatorParam::__FREQ];
  auto freq_mod_amt_t = params[OscillatorParam::__FREQ_MOD_AMT];
  auto pul_width_t = params[OscillatorParam::__PUL_WIDTH];
  auto pul_width_mod_amt_t = params[OscillatorParam::__PUL_WIDTH_MOD_AMT];

  auto freq_mod_t = in_ports[OscillatorInPort::__FREQ_MOD].volt;
  auto pul_width_mod_t = in_ports[OscillatorInPort::__PUL_WIDTH_MOD].volt;
  auto volt_per_oct_t = in_ports[OscillatorInPort::__VOLT_PER_OCT].volt;
  auto sync_t = in_ports[OscillatorInPort::__SYNC].volt;

  auto& sin_t = out_ports[OscillatorOutPort::__SIN].volt;
  auto& tri_t = out_ports[OscillatorOutPort::__TRI].volt;
  auto& saw_t = out_ports[OscillatorOutPort::__SAW].volt;
  auto& sqr_t = out_ports[OscillatorOutPort::__SQR].volt;
  auto& pul_t = out_ports[OscillatorOutPort::__PUL].volt;

  if (freq_tm1 != freq_t) {
    auto stop = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(stop - start);
    std::cout << duration.count() << '\n';
  }
  freq_tm1 = freq_t;

  freq_t *= std::pow(2, volt_per_oct_t + freq_mod_t * freq_mod_amt_t);
  pul_width_t += pul_width_mod_t * pul_width_mod_amt_t;

  freq_t = std::clamp(freq_t, 0.0, freq_sample / 2);
  pul_width_t = std::clamp(pul_width_t, 0.01, 0.99);

  double phase_t = std::fmod(phase_tm1 + freq_t / freq_sample, 1);

  if (sync_tm1 < 0 && sync_t >= 0) {
    phase_t = 0.0;
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
  double sin_t = std::sin(2 * M_PI * phase_t);
  return sin_t;
}

double OscillatorModule::tri(double phase_t) {
  phase_t = std::fmod(phase_t, 1);

  double tri_t =
    phase_t < 0.25 ? 4 * phase_t : (phase_t < 0.75 ? 2 - 4 * phase_t : 4 * phase_t - 4);
  return tri_t;
}

double OscillatorModule::saw(double phase_t) {
  phase_t = std::fmod(phase_t, 1);

  double saw_t = 2 * phase_t - 1;
  return saw_t;
}

double OscillatorModule::sqr(double phase_t) {
  phase_t = std::fmod(phase_t, 1);

  double sqr_t = phase_t < 0.5 ? 1.0 : -1.0;
  return sqr_t;
}

double OscillatorModule::pul(double phase_t, double pul_width_t) {
  phase_t = std::fmod(phase_t, 1);

  double pul_t = phase_t < pul_width_t ? 1.0 : -1.0;
  return pul_t;
}
