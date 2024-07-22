#include <FilterModule.hpp>
#include <cmath>

FilterModule::FilterModule(double freq_sample)
  : AbstractModule{freq_sample},
    params{
      {FilterParam::freq_cut_t, 0},
      {FilterParam::freq_cut_mod_amt_t, 0},
      {FilterParam::res_t, 0},
      {FilterParam::res_mod_amt_t, 0}
    },
    in_ports{
      {FilterInPort::freq_cut_mod_t, 0},
      {FilterInPort::res_mod_t, 0},
      {FilterInPort::in_t, 0}
    },
    out_ports{{FilterOutPort::out_t, 0}},
    in_tm2{0},
    in_tm1{0},
    out_tm2{0},
    out_tm1{0} {}

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
  tmp_tm2 = tmp_tm1;
  tmp_tm1 = tmp_t;

  freq_cut_t *= 1 + freq_cut_mod_t * freq_cut_mod_amt_t;
  res_t *= 1 + res_mod_t * res_mod_t;

  double p = (2 + sqrt(2)) * sqrt(2 - sqrt(2)) / 2;  // 1 / (2 * cos(M_PI / 8))
  double q =
    (2 - sqrt(2)) * sqrt(2 + sqrt(2)) / 2;  // 1 / (2 * cos(3 * M_PI / 8))
  // or maybe just the floats...

  tmp_t = filter(in_tm2, in_tm1, in_t, tmp_tm2, tmp_tm1, freq_cut_t, res_t);
  out_t = filter(tmp_tm2, tmp_tm1, tmp_t, out_tm2, out_tm1, freq_cut_t, res_t);

  in_tm2 = in_tm1;
  in_tm1 = in_t;
}

// higher resonance means moving poles closer radially to the origin
// Q is 1 / (2cos(θ)).

double FilterModule::filter(
  double in_tm2,
  double in_tm1,
  double in_t,
  double out_tm2,
  double out_tm1,
  double freq_cut,
  double res
) {
  double freq_cut_warp = std::tan(M_PI * freq_cut / freq_sample);
  double freq_cut_warp_sqr = freq_cut_warp * freq_cut_warp;

  double b_0 = freq_cut_warp_sqr;
  double b_1 = 2 * freq_cut_warp_sqr;
  double b_2 = freq_cut_warp_sqr;

  double a_0 = 1 + freq_cut_warp / res + freq_cut_warp_sqr;
  double a_1 = 2 * freq_cut_warp_sqr - 2;
  double a_2 = 1 - freq_cut_warp / res + freq_cut_warp_sqr;

  return (b_2 * in_tm2 + b_1 * in_tm1 + b_0 * in_t - a_1 * out_tm1 -
          a_2 * out_tm2) /
         a_0;
}
