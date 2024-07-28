#include <napi.h>
#include <portaudio.h>

#include <chrono>
#include <cmath>
#include <iostream>
#include <memory>
#include <vector>

#include "OscillatorModule.h"

#define FREQ_SAMPLE 44100
#define SAMPLE_SIZE 256

using namespace std;

typedef struct {
  std::vector<std::unique_ptr<OscillatorModule>> modules;
  long tick;
} PaUserData;

// global objects
PaStream *stream;
PaUserData userData;  // this should have read-in params

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

  PaUserData *data = (PaUserData *)userData;
  float *out = (float *)outputBuffer;

  for (unsigned long i = 0; i < SAMPLE_SIZE; i++) {
    data->modules[0]->params[OscillatorModule::OscillatorParam::freq_t] = 440;
    data->modules[0]
      ->params[OscillatorModule::OscillatorParam::freq_mod_amt_t] = 0.0;
    data->modules[0]->params[OscillatorModule::OscillatorParam::pul_width_t] =
      0.5;
    data->modules[0]
      ->params[OscillatorModule::OscillatorParam::pul_width_mod_amt_t] = 0.0;
    data->modules[0]->in_ports[OscillatorModule::OscillatorInPort::oct_t] = 0.0;
    data->modules[0]->in_ports[OscillatorModule::OscillatorInPort::sync_t] =
      0.0;
    data->modules[0]->process();

    *out++ =
      data->modules[0]->out_ports[OscillatorModule::OscillatorOutPort::tri_t];
  }

  auto stop = chrono::high_resolution_clock::now();
  auto duration = chrono::duration_cast<chrono::microseconds>(stop - start);

  if (data->tick % 100 == 0) {
    cout << duration.count() << endl;
  }
  data->tick++;

  return paContinue;
}

void StartStream(const Napi::CallbackInfo &info) {
  Napi::Env env = info.Env();

  PaError err;

  userData.modules.push_back(std::make_unique<OscillatorModule>(FREQ_SAMPLE));
  userData.tick = 0;

  err = Pa_Initialize();
  if (err != paNoError) {
    Napi::Error::New(env, Pa_GetErrorText(err)).ThrowAsJavaScriptException();
  }

  err = Pa_OpenDefaultStream(
    &stream, 0, 1, paFloat32, FREQ_SAMPLE, SAMPLE_SIZE, process, &userData
  );
  if (err != paNoError) {
    Pa_Terminate();
    Napi::Error::New(env, Pa_GetErrorText(err)).ThrowAsJavaScriptException();
  }

  err = Pa_StartStream(stream);
  if (err != paNoError) {
    Pa_CloseStream(stream);
    Pa_Terminate();
    Napi::Error::New(env, Pa_GetErrorText(err)).ThrowAsJavaScriptException();
  }

  std::cout << "Done\n";
  while (true) {}
}

void StopStream(const Napi::CallbackInfo &info) {
  Pa_StopStream(stream);
  Pa_CloseStream(stream);
  Pa_Terminate();
}

Napi::Object Init(Napi::Env env, Napi::Object exports) {
  exports.Set(
    Napi::String::New(env, "startStream"), Napi::Function::New(env, StartStream)
  );
  exports.Set(
    Napi::String::New(env, "stopStream"), Napi::Function::New(env, StopStream)
  );

  return exports;
}

NODE_API_MODULE(NODE_GYP_MODULE_NAME, Init)
