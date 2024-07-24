#include "AmplifierModule.hpp"

#include <algorithm>

AmplifierModule::AmplifierModule(double freq_sample)
  : Module(freq_sample),
    params{
      {AmplifierParam::amp_mod_amt_t, 1.0}
    },
    in_ports{
      {AmplifierInPort::amp_mod_t, 0.0},
      {AmplifierInPort::in_t, 0.0}
    },
    out_ports{
      {AmplifierOutPort::out_t, 0.0}
    } {}

void AmplifierModule::process() {
  auto amp_t = 0.0;
  auto amp_mod_amt_t = params[AmplifierParam::amp_mod_amt_t];

  auto amp_mod_t = in_ports[AmplifierInPort::amp_mod_t];
  auto in_t = in_ports[AmplifierInPort::in_t];

  auto &out_t = out_ports[AmplifierOutPort::out_t];

  amp_t += amp_mod_t * amp_mod_amt_t;

  amp_t = std::clamp(amp_t, 0.0, 1.0);

  out_t = in_t * amp_t;
}
