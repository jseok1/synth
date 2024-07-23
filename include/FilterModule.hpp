#ifndef FILTER_MODULE_HPP
#define FILTER_MODULE_HPP

#include <AbstractModule.hpp>
#include <unordered_map>

class FilterModule : public AbstractModule {
 public:
  enum class FilterParam {
    freq_cut_t,
    freq_cut_mod_amt_t,
    res_t,
    res_mod_amt_t
  };
  enum class FilterInPort {
    freq_cut_mod_t,
    res_mod_t,
    in_t
  };
  enum class FilterOutPort {
    out_t
  };

  std::unordered_map<FilterParam, double> params;
  std::unordered_map<FilterInPort, double> in_ports;
  std::unordered_map<FilterOutPort, double> out_ports;

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
