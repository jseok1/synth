#ifndef FILTER_MODULE_HPP
#define FILTER_MODULE_HPP

#include <unordered_map>

#include "modules/Module.hpp"

class FilterModule : public Module {
 public:
  enum FilterParam : int {
    __FREQ_CUT,
    __FREQ_CUT_MOD_AMT,
    __RES,
    __RES_MOD_AMT
  };
  enum FilterInPort : int {
    __FREQ_CUT_MOD,
    __RES_MOD,
    __IN
  };
  enum FilterOutPort : int {
    __OUT
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
