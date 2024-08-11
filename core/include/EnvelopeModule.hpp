#ifndef ENVELOPE_MODULE_H
#define ENVELOPE_MODULE_H

#include <unordered_map>

#include "Module.hpp"

class EnvelopeModule : public Module {
 public:
  enum EnvelopeParam : int {
    att_t,
    att_mod_amt_t,
    dec_t,
    dec_mod_amt_t,
    sus_t,
    sus_mod_amt_t,
    rel_t,
    rel_mod_amt_t
  };
  enum EnvelopeInPort : int {
    att_mod_t,
    dec_mod_t,
    sus_mod_t,
    rel_mod_t,
    gate_t,
    retr_t
  };
  enum EnvelopeOutPort : int {
    env_t
  };

  EnvelopeModule(double freq_sample);

  void process() override;

 private:
  enum EnvelopeStage : int {
    att,
    dec,
    rel,
    sus,
    idl
  };

  int stage_tm1;
  double sus_tm1;
  double gate_tm1;
  double retr_tm1;
  double env_tm1;

  static double env(
    double env_tm1,
    int stage_t,
    double att_t,
    double dec_t,
    double sus_t,
    double rel_t
  );
};

#endif
