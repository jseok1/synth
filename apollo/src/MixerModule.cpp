#include <MixerModule.hpp>

MixerModule::MixerModule(double freq_sample) : AbstractModule{freq_sample} {}

void MixerModule::process() {
  double in_1_t = in_ports[IN_1_T];
  double in_2_t = in_ports[IN_2_T];

  double &out_t = out_ports[OUT_T];

  double gain = 1.f;  // initial level?
  gain /= 2.f;        // divide by number of ports

  // interesting consideration -- this module needs to know whether there's
  // actually a signal connected

  out_t = (in_1_t + in_2_t) * gain;
}
