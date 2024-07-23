#include <FilterModule.hpp>
#include <algorithm>
#include <cmath>

FilterModule::FilterModule(double freq_sample)
  : Module{freq_sample},
    params{
      {FilterParam::freq_cut_t, 0.0},
      {FilterParam::freq_cut_mod_amt_t, 0.0},
      {FilterParam::res_t, 0.0},
      {FilterParam::res_mod_amt_t, 0.0}
    },
    in_ports{
      {FilterInPort::freq_cut_mod_t, 0.0},
      {FilterInPort::res_mod_t, 0.0},
      {FilterInPort::in_t, 0.0}
    },
    out_ports{{FilterOutPort::out_t, 0.0}},
    in_tm2{0.0},
    in_tm1{0.0},
    out_tm2{0.0},
    out_tm1{0.0},
    hidden_tm2{0.0},
    hidden_tm1{0.0},
    hidden_t{0.0} {}

void FilterModule::process() {
  auto freq_cut_t = params[FilterParam::freq_cut_t];
  auto freq_cut_mod_amt_t = params[FilterParam::freq_cut_mod_amt_t];
  auto res_t = params[FilterParam::res_t];
  auto res_mod_amt_t = params[FilterParam::res_mod_amt_t];

  auto freq_cut_mod_t = in_ports[FilterInPort::freq_cut_mod_t];
  auto res_mod_t = in_ports[FilterInPort::res_mod_t];
  auto in_t = in_ports[FilterInPort::in_t];

  auto &out_t = out_ports[FilterOutPort::out_t];

  out_tm2 = out_tm1;
  out_tm1 = out_t;
  hidden_tm2 = hidden_tm1;
  hidden_tm1 = hidden_t;

  freq_cut_t *= 1 + freq_cut_mod_t * freq_cut_mod_amt_t;
  res_t *= 1 + res_mod_t * res_mod_t;

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
