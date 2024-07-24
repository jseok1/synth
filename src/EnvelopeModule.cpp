#include "EnvelopeModule.hpp"

#include <algorithm>
#include <cmath>
#include <stdexcept>

EnvelopeModule::EnvelopeModule(double freq_sample)
  : Module{freq_sample},
    params{
      {EnvelopeParam::att_t, 0.0},
      {EnvelopeParam::att_mod_amt_t, 0.0},
      {EnvelopeParam::dec_t, 0.0},
      {EnvelopeParam::dec_mod_amt_t, 0.0},
      {EnvelopeParam::sus_t, 0.0},
      {EnvelopeParam::sus_mod_amt_t, 0.0},
      {EnvelopeParam::rel_t, 0.0},
      {EnvelopeParam::rel_mod_amt_t, 0.0}
    },
    in_ports{
      {EnvelopeInPort::att_mod_t, 0.0},
      {EnvelopeInPort::dec_mod_t, 0.0},
      {EnvelopeInPort::sus_mod_t, 0.0},
      {EnvelopeInPort::rel_mod_t, 0.0},
      {EnvelopeInPort::gate_t, 0.0},
      {EnvelopeInPort::retr_t, 0.0}
    },
    out_ports{
      {EnvelopeOutPort::env_t, 0.0}
    },
    stage_tm1{EnvelopeStage::idl},
    sus_tm1{0.0},
    gate_tm1{0.0},
    retr_tm1{0.0},
    env_tm1{0.0} {}

void EnvelopeModule::process() {
  auto att_t = params[EnvelopeParam::att_t];
  auto att_mod_amt_t = params[EnvelopeParam::att_mod_amt_t];
  auto dec_t = params[EnvelopeParam::dec_t];
  auto dec_mod_amt_t = params[EnvelopeParam::dec_mod_amt_t];
  auto sus_t = params[EnvelopeParam::sus_t];
  auto sus_mod_amt_t = params[EnvelopeParam::sus_mod_amt_t];
  auto rel_t = params[EnvelopeParam::rel_t];
  auto rel_mod_amt_t = params[EnvelopeParam::rel_mod_amt_t];

  auto att_mod_t = in_ports[EnvelopeInPort::att_mod_t];
  auto dec_mod_t = in_ports[EnvelopeInPort::dec_mod_t];
  auto sus_mod_t = in_ports[EnvelopeInPort::sus_mod_t];
  auto rel_mod_t = in_ports[EnvelopeInPort::rel_mod_t];
  auto gate_t = in_ports[EnvelopeInPort::gate_t];
  auto retr_t = in_ports[EnvelopeInPort::retr_t];

  auto &env_t = out_ports[EnvelopeOutPort::env_t];

  env_tm1 = env_t;

  att_t += att_mod_t * att_mod_amt_t;
  dec_t += dec_mod_t * dec_mod_amt_t;
  sus_t += sus_mod_t * sus_mod_amt_t;
  rel_t += rel_mod_t * rel_mod_amt_t;

  att_t = std::clamp(att_t, 0.0, 1.0) * freq_sample * 10;
  dec_t = std::clamp(dec_t, 0.0, 1.0) * freq_sample * 10;
  sus_t = std::clamp(sus_t, 0.0, 1.0) * freq_sample * 10;
  rel_t = std::clamp(rel_t, 0.0, 1.0) * freq_sample * 10;

  EnvelopeStage stage_t;
  switch (stage_tm1) {
    case EnvelopeStage::att:
      stage_t = env_tm1 == 1 ? EnvelopeStage::dec : EnvelopeStage::att;
      break;
    case EnvelopeStage::dec:
      stage_t = env_tm1 == sus_tm1 ? EnvelopeStage::sus : EnvelopeStage::dec;
      break;
    case EnvelopeStage::sus:
      stage_t = EnvelopeStage::sus;
      break;
    case EnvelopeStage::rel:
      stage_t = env_tm1 == 0 ? EnvelopeStage::idl : EnvelopeStage::rel;
      break;
    case EnvelopeStage::idl:
      stage_t = EnvelopeStage::idl;
      break;
    default:
      throw std::invalid_argument("EnvelopeStage is invalid.");
  }

  if (!gate_tm1 && gate_t || !retr_tm1 && retr_t) {
    stage_t = EnvelopeStage::att;
  }
  if (gate_tm1 && !gate_t) {
    stage_t = EnvelopeStage::rel;
  }

  env_t = env(env_tm1, stage_t, att_t, dec_t, sus_t, rel_t);

  stage_tm1 = stage_t;
  sus_tm1 = sus_t;
  gate_tm1 = gate_t;
  retr_tm1 = retr_t;
}

double EnvelopeModule::env(
  double env_tm1,
  EnvelopeStage stage_t,
  double att_t,
  double dec_t,
  double sus_t,
  double rel_t
) {
  double env_t;
  switch (stage_t) {
    case EnvelopeStage::att:
      double att_target_t = 1.2;
      double att_rate_t = std::log((att_target_t - 1) / att_target_t) / att_t;
      env_t = std::min(
        (env_tm1 - att_target_t) * std::exp(att_rate_t) + att_target_t, 1.0
      );
      break;
    case EnvelopeStage::dec:
      double dec_target_t = sus_t - 0.001;
      double dec_rate_t = -std::log((dec_target_t - 1) / dec_target_t) / dec_t;
      env_t = std::max(
        (env_tm1 - dec_target_t) * std::exp(dec_rate_t) + dec_target_t, sus_t
      );
      break;
    case EnvelopeStage::sus:
      env_t = sus_t;
      break;
    case EnvelopeStage::rel:
      double rel_target_t = -0.001;
      double rel_rate_t = -std::log((rel_target_t - 1) / rel_target_t) / rel_t;
      env_t = std::max(
        (env_tm1 - rel_target_t) * std::exp(rel_rate_t) + rel_target_t, 0.0
      );
      break;
    case EnvelopeStage::idl:
      env_t = 0.0;
      break;
    default:
      throw std::invalid_argument("EnvelopeStage is invalid.");
  }

  return env_t;
}
