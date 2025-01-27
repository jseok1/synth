#include "modules/FilterModule.hpp"

#include <algorithm>
#include <cmath>

FilterModule::FilterModule(double freq_sample)
  : Module{freq_sample, {
      {FilterParam::__FREQ_CUT, 20.0},
      {FilterParam::__FREQ_CUT_MOD_AMT, 0.0},
      {FilterParam::__RES, 0.0},
      {FilterParam::__RES_MOD_AMT, 0.0}
    }, {
      {FilterInPort::__FREQ_CUT_MOD, InPort{0.0, false}},
      {FilterInPort::__RES_MOD, InPort{0.0, false}},
      {FilterInPort::__IN, InPort{0.0, false}}
    }, {
      {FilterOutPort::__OUT, OutPort{0.0}}
    }},
    in_tm2{0.0},
    in_tm1{0.0},
    out_tm2{0.0},
    out_tm1{0.0},
    hidden_tm2{0.0},
    hidden_tm1{0.0},
    hidden_t{0.0} {}

void FilterModule::process() {
  auto freq_cut_t = params[FilterParam::__FREQ_CUT];
  auto freq_cut_mod_amt_t = params[FilterParam::__FREQ_CUT_MOD_AMT];
  auto res_t = params[FilterParam::__RES];
  auto res_mod_amt_t = params[FilterParam::__RES_MOD_AMT];

  auto freq_cut_mod_t = in_ports[FilterInPort::__FREQ_CUT_MOD].volt;
  auto res_mod_t = in_ports[FilterInPort::__RES_MOD].volt;
  auto in_t = in_ports[FilterInPort::__IN].volt;

  auto &out_t = out_ports[FilterOutPort::__OUT].volt;

  out_tm2 = out_tm1;
  out_tm1 = out_t;
  hidden_tm2 = hidden_tm1;
  hidden_tm1 = hidden_t;

  freq_cut_t *= std::pow(2, freq_cut_mod_t * freq_cut_mod_amt_t);
  res_t += res_mod_t * res_mod_t;

  freq_cut_t = std::clamp(freq_cut_t, 0.0, freq_sample / 2);
  res_t = std::clamp(res_t, 0.0, 0.99);

  freq_cut_t = std::tan(M_PI * freq_cut_t / freq_sample);

  double qual_t;

  qual_t = 1 / (2 * std::cos(M_PI / 8 * (1 + res_t / 3)));
  hidden_t = filter(in_tm2, in_tm1, in_t, hidden_tm2, hidden_tm1, freq_cut_t, qual_t);

  qual_t = 1 / (2 * std::cos(3 * M_PI / 8 * (1 + res_t / 3)));
  out_t = filter(hidden_tm2, hidden_tm1, hidden_t, out_tm2, out_tm1, freq_cut_t, qual_t);

  in_tm2 = in_tm1;
  in_tm1 = in_t;
}

double FilterModule::filter(
  double in_tm2,
  double in_tm1,
  double in_t,
  double out_tm2,
  double out_tm1,
  double freq_cut_t,
  double qual_t
) {
  double freq_cut_sqr_t = freq_cut_t * freq_cut_t;

  double out_t = 0.0;
  out_t += freq_cut_sqr_t * in_tm2;
  out_t += 2 * freq_cut_sqr_t * in_tm1;
  out_t += freq_cut_sqr_t * in_t;
  out_t -= (1 - freq_cut_t / qual_t + freq_cut_sqr_t) * out_tm2;
  out_t -= (2 * freq_cut_sqr_t - 2) * out_tm1;
  out_t /= (1 + freq_cut_t / qual_t + freq_cut_sqr_t);

  return out_t;
}

// TODO: make order of filter a param? and see how you can generalize?
// cascades
