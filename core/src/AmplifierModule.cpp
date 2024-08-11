#include "AmplifierModule.h"

#include <algorithm>

AmplifierModule::AmplifierModule(double freq_sample)
  : Module{freq_sample, {
      {AmplifierParam::amp_mod_amt_t, 1.0}
    }, {
      {AmplifierInPort::amp_mod_t, InPort{0.0, false}},
      {AmplifierInPort::in_t, InPort{0.0, false}}
    }, {
      {AmplifierOutPort::out_t, OutPort{0.0}}
    }} {}

void AmplifierModule::process() {
  auto amp_t = 0.0;
  auto amp_mod_amt_t = params[AmplifierParam::amp_mod_amt_t];

  auto amp_mod_t = in_ports[AmplifierInPort::amp_mod_t].volt;
  auto in_t = in_ports[AmplifierInPort::in_t].volt;

  auto &out_t = out_ports[AmplifierOutPort::out_t].volt;

  if (!in_ports[AmplifierInPort::amp_mod_t].is_connected) {
    amp_mod_t = 1.0;
  }

  amp_t += amp_mod_t * amp_mod_amt_t;

  amp_t = std::clamp(amp_t, 0.0, 1.0);

  out_t = in_t * amp_t;
}
