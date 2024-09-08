#ifndef ENVELOPE_MODULE_HPP
#define ENVELOPE_MODULE_HPP

#include <unordered_map>

#include "modules/Module.hpp"

class EnvelopeModule : public Module {
 public:
  enum EnvelopeParam : int {
    __ATT,
    __ATT_MOD_AMT,
    __DEC,
    __DEC_MOD_AMT,
    __SUS,
    __SUS_MOD_AMT,
    __REL,
    __REL_MOD_AMT
  };
  enum EnvelopeInPort : int {
    __ATT_MOD,
    __DEC_MOD,
    __SUS_MOD,
    __REL_MOD,
    __GATE,
    __RETR
  };
  enum EnvelopeOutPort : int {
    __ENV
  };

  EnvelopeModule(double freq_sample);

  void process() override;

 private:
  enum EnvelopeStage : int {
    __ATT_STAGE,
    __DEC_STAGE,
    __REL_STAGE,
    __SUS_STAGE,
    __IDL_STAGE
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
