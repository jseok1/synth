#include "modules/MixerModule.hpp"

#include <algorithm>

MixerModule::MixerModule(double freq_sample)
  : Module{
      freq_sample,
      {{MixerParam::__AMP_MOD_AMT_1, 1.0},
       {MixerParam::__AMP_MOD_AMT_2, 1.0},
       {MixerParam::__AMP_MOD_AMT_3, 1.0},
       {MixerParam::__AMP_MOD_AMT_4, 1.0}},
      {{MixerInPort::__IN_1, InPort{0.0, false}},
       {MixerInPort::__IN_2, InPort{0.0, false}},
       {MixerInPort::__IN_3, InPort{0.0, false}},
       {MixerInPort::__IN_4, InPort{0.0, false}}},
      {{MixerOutPort::__OUT, OutPort{0.0}}}
    } {}

void MixerModule::process() {
  auto amp_1_t = 0.0;
  auto amp_mod_amt_1_t = params[MixerParam::__AMP_MOD_AMT_1];
  auto amp_2_t = 0.0;
  auto amp_mod_amt_2_t = params[MixerParam::__AMP_MOD_AMT_2];
  auto amp_3_t = 0.0;
  auto amp_mod_amt_3_t = params[MixerParam::__AMP_MOD_AMT_3];
  auto amp_4_t = 0.0;
  auto amp_mod_amt_4_t = params[MixerParam::__AMP_MOD_AMT_4];

  auto amp_mod_1_t = 1.0;
  auto in_1_t = in_ports[MixerInPort::__IN_1].volt;
  auto amp_mod_2_t = 1.0;
  auto in_2_t = in_ports[MixerInPort::__IN_2].volt;
  auto amp_mod_3_t = 1.0;
  auto in_3_t = in_ports[MixerInPort::__IN_3].volt;
  auto amp_mod_4_t = 1.0;
  auto in_4_t = in_ports[MixerInPort::__IN_4].volt;

  auto &out_t = out_ports[MixerOutPort::__OUT].volt;

  amp_1_t += amp_mod_1_t * amp_mod_amt_1_t;
  amp_2_t += amp_mod_2_t * amp_mod_amt_2_t;
  amp_3_t += amp_mod_3_t * amp_mod_amt_3_t;
  amp_4_t += amp_mod_4_t * amp_mod_amt_4_t;

  amp_1_t = std::clamp(amp_1_t, 0.0, 1.0);
  amp_2_t = std::clamp(amp_2_t, 0.0, 1.0);
  amp_3_t = std::clamp(amp_3_t, 0.0, 1.0);
  amp_4_t = std::clamp(amp_4_t, 0.0, 1.0);

  // TODO: normalize
  out_t = in_1_t * amp_1_t + in_2_t * amp_2_t + in_3_t * amp_3_t + in_4_t * amp_4_t;
}
