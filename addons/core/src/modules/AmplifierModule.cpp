#include "modules/AmplifierModule.hpp"

#include <algorithm>

AmplifierModule::AmplifierModule(double freq_sample)
  : Module{freq_sample, {
      {AmplifierParam::__AMP_MOD_AMT, 1.0}
    }, {
      {AmplifierInPort::__AMP_MOD, InPort{0.0, false}},
      {AmplifierInPort::__IN, InPort{0.0, false}}
    }, {
      {AmplifierOutPort::__OUT, OutPort{0.0}}
    }} {}

void AmplifierModule::process() {
  auto amp_t = 0.0;
  auto amp_mod_amt_t = params[AmplifierParam::__AMP_MOD_AMT];

  auto amp_mod_t = in_ports[AmplifierInPort::__AMP_MOD].volt;
  auto in_t = in_ports[AmplifierInPort::__IN].volt;

  auto &out_t = out_ports[AmplifierOutPort::__OUT].volt;

  if (!in_ports[AmplifierInPort::__AMP_MOD].is_connected) {
    amp_mod_t = 1.0;
  }

  amp_t += amp_mod_t * amp_mod_amt_t;

  amp_t = std::clamp(amp_t, 0.0, 1.0);

  out_t = in_t * amp_t;
}
