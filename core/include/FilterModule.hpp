#ifndef FILTER_MODULE_H
#define FILTER_MODULE_H

#include <unordered_map>

#include "Module.hpp"

class FilterModule : public Module {
 public:
  enum FilterParam : int {
    freq_cut_t,
    freq_cut_mod_amt_t,
    res_t,
    res_mod_amt_t
  };
  enum FilterInPort : int {
    freq_cut_mod_t,
    res_mod_t,
    in_t
  };
  enum FilterOutPort : int {
    out_t
  };

  FilterModule(double freq_sample);

  void process() override;

 private:
  double in_tm2;
  double in_tm1;
  double out_tm2;
  double out_tm1;
  double hidden_tm2;
  double hidden_tm1;
  double hidden_t;

  static double filter(
    double in_tm2,
    double in_tm1,
    double in_t,
    double out_tm2,
    double out_tm1,
    double freq_cut_t,
    double qual_t
  );
};

#endif
