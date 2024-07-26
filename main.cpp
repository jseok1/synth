#include <chrono>
#include <cmath>
#include <iostream>
#include <portaudio.h>

#include "OscillatorModule.hpp"
#include "MixerModule.hpp"
#include "FilterModule.hpp"

#define FREQ_SAMPLE 44100
#define SAMPLE_SIZE 256

using namespace std;

typedef struct {
  OscillatorModule *oscillator1;
  OscillatorModule *oscillator2;
  MixerModule *mixer;
  FilterModule *filter;
  long tick;
} PaTestData;

// 0.0058 at 256 samples.
// 0.000100 + osc
// 0.000250 + osc, filter (down to 0.000180)
static int process(
  const void *inputBuffer,
  void *outputBuffer,
  unsigned long framesPerBuffer,
  const PaStreamCallbackTimeInfo *timeInfo,
  PaStreamCallbackFlags statusFlags,
  void *userData
) {
  (void)inputBuffer;
  (void)framesPerBuffer;

  auto start = chrono::high_resolution_clock::now();

  PaTestData *data = (PaTestData *)userData;
  float *out = (float *)outputBuffer;

  for (unsigned long i = 0; i < SAMPLE_SIZE; i++) {
    data->oscillator1->params[OscillatorModule::OscillatorParam::freq_t] = 440.0;
    data->oscillator1->params[OscillatorModule::OscillatorParam::freq_mod_amt_t] = 0.0;
    data->oscillator1->params[OscillatorModule::OscillatorParam::pul_width_t] = 0.5;
    data->oscillator1->params[OscillatorModule::OscillatorParam::pul_width_mod_amt_t] = 0.0;
    data->oscillator1->in_ports[OscillatorModule::OscillatorInPort::oct_t] = 0.0;
    data->oscillator1->in_ports[OscillatorModule::OscillatorInPort::sync_t] = 0.0;
    data->oscillator1->process();
    
    *out++ = data->oscillator1->out_ports[OscillatorModule::OscillatorOutPort::sqr_t];

    // data->oscillator2->params[OscillatorModule::OscillatorParam::freq_t] = 320.0;
    // data->oscillator2->params[OscillatorModule::OscillatorParam::freq_mod_amt_t] = 0.0;
    // data->oscillator2->params[OscillatorModule::OscillatorParam::pul_width_t] = 0.5;
    // data->oscillator2->params[OscillatorModule::OscillatorParam::pul_width_mod_amt_t] = 0.0;
    // data->oscillator2->in_ports[OscillatorModule::OscillatorInPort::oct_t] = 0.0;
    // data->oscillator2->in_ports[OscillatorModule::OscillatorInPort::sync_t] = data->oscillator1->out_ports[OscillatorModule::OscillatorOutPort::sqr_t];
    // data->oscillator2->process();

    // data->mixer->in_ports[MixerModule::MixerInPort::] = data->oscillator1->out_ports[OscillatorModule::SQR_T];
    // data->mixer->in_ports[MixerModule::IN_2_T] = data->oscillator2->out_ports[OscillatorModule::SAW_T];
    // data->mixer->process();

    // data->filter->params[FilterModule::FREQ_CUT_T] = 1000.0;
    // data->filter->params[FilterModule::FREQ_CUT_MOD_AMT_T] = 0.0;
    // data->filter->params[FilterModule::RES_T] = 1 / sqrt(2);
    // data->filter->params[FilterModule::RES_MOD_AMT_T] = 0.0;
    // data->filter->in_ports[FilterModule::IN_T] = data->mixer->out_ports[MixerModule::OUT_T];
    // data->filter->process();

    // *out++ = data->filter->out_ports[FilterModule::OUT_T];
  }

  auto stop = chrono::high_resolution_clock::now();
  auto duration = chrono::duration_cast<chrono::microseconds>(stop - start);

  if (data->tick % 100 == 0) {
    cout << duration.count() << endl;
  }
  data->tick++;

  return paContinue;
}

int main() {
  PaStream *stream;
  PaError err;

  OscillatorModule oscillator1(FREQ_SAMPLE);
  OscillatorModule oscillator2(FREQ_SAMPLE);
  MixerModule mixer(FREQ_SAMPLE);
  FilterModule filter(FREQ_SAMPLE);
  PaTestData data;
  data.oscillator1 = &oscillator1;
  data.oscillator2 = &oscillator2;
  data.mixer = &mixer;
  data.filter = &filter;
  data.tick = 0;

  err = Pa_Initialize();
  if (err != paNoError) {
    cerr << "PortAudio error: " << Pa_GetErrorText(err) << endl;
    return 1;
  }

  // Open audio stream
  err = Pa_OpenDefaultStream(
    &stream,
    0,          // no input channels
    1,          // mono output
    paFloat32,  // 32-bit floating point output
    FREQ_SAMPLE,
    SAMPLE_SIZE,
    process,
    &data
  );
  if (err != paNoError) {
    cerr << "PortAudio error: " << Pa_GetErrorText(err) << endl;
    Pa_Terminate();
    return 1;
  }

  err = Pa_StartStream(stream);
  if (err != paNoError) {
    cerr << "PortAudio error: " << Pa_GetErrorText(err) << endl;
    Pa_CloseStream(stream);
    Pa_Terminate();
    return 1;
  }

  cout << "Playing sound. Press Enter to stop." << endl;
  cin.get();

  err = Pa_StopStream(stream);
  if (err != paNoError) {
    cerr << "PortAudio error: " << Pa_GetErrorText(err) << endl;
  }

  err = Pa_CloseStream(stream);
  if (err != paNoError) {
    cerr << "PortAudio error: " << Pa_GetErrorText(err) << endl;
  }

  Pa_Terminate();

  return 0;
}
