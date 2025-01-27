#include "modules/EnvelopeModule.hpp"

#include <algorithm>
#include <cmath>
#include <stdexcept>

EnvelopeModule::EnvelopeModule(double freq_sample)
  : Module{freq_sample, {
      {EnvelopeParam::__ATT, 0.0},
      {EnvelopeParam::__ATT_MOD_AMT, 0.0},
      {EnvelopeParam::__DEC, 0.0},
      {EnvelopeParam::__DEC_MOD_AMT, 0.0},
      {EnvelopeParam::__SUS, 0.0},
      {EnvelopeParam::__SUS_MOD_AMT, 0.0},
      {EnvelopeParam::__REL, 0.0},
      {EnvelopeParam::__REL_MOD_AMT, 0.0}
    }, {
      {EnvelopeInPort::__ATT_MOD, InPort{0.0, false}},
      {EnvelopeInPort::__DEC_MOD, InPort{0.0, false}},
      {EnvelopeInPort::__SUS_MOD, InPort{0.0, false}},
      {EnvelopeInPort::__REL_MOD, InPort{0.0, false}},
      {EnvelopeInPort::__GATE, InPort{0.0, false}},
      {EnvelopeInPort::__RETR, InPort{0.0, false}}
    }, {
      {EnvelopeOutPort::__ENV, OutPort{0.0}}
    }},
    stage_tm1{EnvelopeStage::__IDL_STAGE},
    sus_tm1{0.0},
    gate_tm1{0.0},
    retr_tm1{0.0},
    env_tm1{0.0} {}

void EnvelopeModule::process() {
  auto att_t = params[EnvelopeParam::__ATT];
  auto att_mod_amt_t = params[EnvelopeParam::__ATT_MOD_AMT];
  auto dec_t = params[EnvelopeParam::__DEC];
  auto dec_mod_amt_t = params[EnvelopeParam::__DEC_MOD_AMT];
  auto sus_t = params[EnvelopeParam::__SUS];
  auto sus_mod_amt_t = params[EnvelopeParam::__SUS_MOD_AMT];
  auto rel_t = params[EnvelopeParam::__REL];
  auto rel_mod_amt_t = params[EnvelopeParam::__REL_MOD_AMT];

  auto att_mod_t = in_ports[EnvelopeInPort::__ATT_MOD].volt;
  auto dec_mod_t = in_ports[EnvelopeInPort::__DEC_MOD].volt;
  auto sus_mod_t = in_ports[EnvelopeInPort::__SUS_MOD].volt;
  auto rel_mod_t = in_ports[EnvelopeInPort::__REL_MOD].volt;
  auto gate_t = in_ports[EnvelopeInPort::__GATE].volt;
  auto retr_t = in_ports[EnvelopeInPort::__RETR].volt;

  auto &env_t = out_ports[EnvelopeOutPort::__ENV].volt;

  env_tm1 = env_t;

  att_t += att_mod_t * att_mod_amt_t;
  dec_t += dec_mod_t * dec_mod_amt_t;
  sus_t += sus_mod_t * sus_mod_amt_t;
  rel_t += rel_mod_t * rel_mod_amt_t;

  att_t = std::clamp(att_t, 0.0, 1.0) * freq_sample * 10;
  dec_t = std::clamp(dec_t, 0.0, 1.0) * freq_sample * 10;
  sus_t = std::clamp(sus_t, 0.0, 1.0) * freq_sample * 10;
  rel_t = std::clamp(rel_t, 0.0, 1.0) * freq_sample * 10;

  int stage_t;
  switch (stage_tm1) {
    case EnvelopeStage::__ATT_STAGE: {
      stage_t = env_tm1 == 1 ? EnvelopeStage::__DEC_STAGE : EnvelopeStage::__ATT_STAGE;
      break;
    }
    case EnvelopeStage::__DEC_STAGE: {
      stage_t = env_tm1 == sus_tm1 ? EnvelopeStage::__SUS_STAGE : EnvelopeStage::__DEC_STAGE;
      break;
    }
    case EnvelopeStage::__SUS_STAGE: {
      stage_t = EnvelopeStage::__SUS_STAGE;
      break;
    }
    case EnvelopeStage::__REL_STAGE: {
      stage_t = env_tm1 == 0 ? EnvelopeStage::__IDL_STAGE : EnvelopeStage::__REL_STAGE;
      break;
    }
    case EnvelopeStage::__IDL_STAGE: {
      stage_t = EnvelopeStage::__IDL_STAGE;
      break;
    }
    default: {
      throw std::invalid_argument("ERROR::ENVELOPE_MODULE::ENVELOPE_STAGE_INVALID");
    }
  }

  if (!gate_tm1 && gate_t || !retr_tm1 && retr_t) {
    stage_t = EnvelopeStage::__ATT_STAGE;
  }
  if (gate_tm1 && !gate_t) {
    stage_t = EnvelopeStage::__REL_STAGE;
  }

  env_t = env(env_tm1, stage_t, att_t, dec_t, sus_t, rel_t);

  stage_tm1 = stage_t;
  sus_tm1 = sus_t;
  gate_tm1 = gate_t;
  retr_tm1 = retr_t;
}

double EnvelopeModule::env(
  double env_tm1,
  int stage_t,
  double att_t,
  double dec_t,
  double sus_t,
  double rel_t
) {
  double env_t;
  switch (stage_t) {
    case EnvelopeStage::__ATT_STAGE: {
      double att_target_t = 1.2;
      double att_rate_t = std::log((att_target_t - 1) / att_target_t) / att_t;
      env_t = std::min((env_tm1 - att_target_t) * std::exp(att_rate_t) + att_target_t, 1.0);
      break;
    }
    case EnvelopeStage::__DEC_STAGE: {
      double dec_target_t = sus_t - 0.001;
      double dec_rate_t = -std::log((dec_target_t - 1) / dec_target_t) / dec_t;
      env_t = std::max((env_tm1 - dec_target_t) * std::exp(dec_rate_t) + dec_target_t, sus_t);
      break;
    }
    case EnvelopeStage::__SUS_STAGE: {
      env_t = sus_t;
      break;
    }
    case EnvelopeStage::__REL_STAGE: {
      double rel_target_t = -0.001;
      double rel_rate_t = -std::log((rel_target_t - 1) / rel_target_t) / rel_t;
      env_t = std::max((env_tm1 - rel_target_t) * std::exp(rel_rate_t) + rel_target_t, 0.0);
      break;
    }
    case EnvelopeStage::__IDL_STAGE: {
      env_t = 0.0;
      break;
    }
    default: {
      throw std::invalid_argument("ERROR::ENVELOPE_MODULE::ENVELOPE_STAGE_INVALID");
    }
  }

  return env_t;
}
