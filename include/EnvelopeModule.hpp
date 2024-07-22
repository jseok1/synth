#ifndef ENVELOPE_MODULE_HPP
#define ENVELOPE_MODULE_HPP

#include <AbstractModule.hpp>
#include <unordered_map>

class EnvelopeModule : public AbstractModule {
 public:
  enum class EnvelopeParam {
    att_t,
    att_mod_amt_t,
    dec_t,
    dec_mod_amt_t,
    sus_t,
    sus_mod_amt_t,
    rel_t,
    rel_mod_amt_t
  };
  enum class EnvelopeInPort {
    att_mod_t,
    dec_mod_t,
    sus_mod_t,
    rel_mod_t,
    gate_t,
    retr_t
  };
  enum class EnvelopeOutPort {
    env_t
  };

  std::unordered_map<EnvelopeParam, double> params;
  std::unordered_map<EnvelopeInPort, double> in_ports;
  std::unordered_map<EnvelopeOutPort, double> out_ports;

  EnvelopeModule(double freq_sample);
  void process() override;

 private:
  enum class EnvelopeStage {
    att,
    dec,
    rel,
    sus,
    idl
  };

  EnvelopeStage stage_tm1;
  double sus_tm1;
  double gate_tm1;
  double retr_tm1;
  double env_tm1;

  static double env(
    double env_tm1,
    EnvelopeStage stage_t,
    double att_t,
    double dec_t,
    double sus_t,
    double rel_t
  );
};

#endif
