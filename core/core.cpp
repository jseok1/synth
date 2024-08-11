#include <napi.h>

#include <atomic>
#include <chrono>
#include <cmath>
#include <iostream>
#include <memory>
#include <thread>
#include <vector>

#include "Module.h"
#include "OscillatorModule.h"
#include "portaudio/portaudio.h"

#define FREQ_SAMPLE 44100
#define SAMPLE_SIZE 256

// modules graph
// modules
//

typedef struct {
  std::vector<std::shared_ptr<Module>> modules;
  std::vector<float> params;
  bool running;
  long tick;
} PaUserData;

std::atomic<bool *> pointer;  // raw atomic ptr to obj
std::unique_ptr<bool>
  storage;  // place for holding ptr while the other is null and handles auto memory management

static int streamCallback(
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

  auto *current_pointer = pointer.exchange(nullptr);

  PaUserData *data = (PaUserData *)userData;
  float *out = (float *)outputBuffer;

  for (unsigned long i = 0; i < SAMPLE_SIZE; i++) {
    data->modules[0]->params[OscillatorModule::OscillatorParam::freq_t] = 440;
    data->modules[0]->params[OscillatorModule::OscillatorParam::freq_mod_amt_t] = 0.0;
    data->modules[0]->params[OscillatorModule::OscillatorParam::pul_width_t] = 0.5;
    data->modules[0]->params[OscillatorModule::OscillatorParam::pul_width_mod_amt_t] = 0.0;
    data->modules[0]->in_ports[OscillatorModule::OscillatorInPort::oct_t] = 0.0;
    data->modules[0]->in_ports[OscillatorModule::OscillatorInPort::sync_t] = 0.0;
    data->modules[0]->process();

    *out++ = data->modules[0]->out_ports[OscillatorModule::OscillatorOutPort::tri_t];
  }

  auto stop = chrono::high_resolution_clock::now();
  auto duration = chrono::duration_cast<chrono::microseconds>(stop - start);

  if (data->tick % 100 == 0) {
    std::cout << duration.count() << '\n';
  }
  data->tick++;

  int flag = data->running ? paContinue : paComplete;

  pointer.store(current_pointer);

  return flag;
}

void StartStream(const Napi::CallbackInfo &info) {
  auto main = []() {
    PaError err;

    userData.modules.push_back(std::make_unique<OscillatorModule>(FREQ_SAMPLE));
    userData.running = true;
    userData.tick = 0;

    err = Pa_Initialize();
    if (err != paNoError) {
      std::cout << Pa_GetErrorText(err) << '\n';
      return;
    }

    PaStream *stream;
    err = Pa_OpenDefaultStream(
      &stream, 0, 1, paFloat32, FREQ_SAMPLE, SAMPLE_SIZE, streamCallback, &userData
    );
    if (err != paNoError) {
      Pa_Terminate();
      std::cout << Pa_GetErrorText(err) << '\n';
      return;
    }

    err = Pa_StartStream(stream);
    if (err != paNoError) {
      Pa_Terminate();
      std::cout << Pa_GetErrorText(err) << '\n';
      return;
    }

    while ((err = Pa_IsStreamActive(stream)) == 1) {
      Pa_Sleep(100);
    }
    if (err != paNoError) {
      Pa_Terminate();
      std::cout << Pa_GetErrorText(err) << '\n';
      return;
    }

    err = Pa_CloseStream(stream);
    if (err != paNoError) {
      Pa_Terminate();
      std::cout << Pa_GetErrorText(err) << '\n';
      return;
    }

    Pa_Terminate();
  };

  std::thread{main}.detach();
}

void StopStream(const Napi::CallbackInfo &info) {
  // I think I can read here (since consumer is read-only and there is only one
  // producer)
  auto copy = *storage;
  copy.running = false;

  auto desired = std::make_unique<PaUserData>(copy);
  for (auto *expected = storage.get(); !pointer.compare_exchange_weak(expected, desired.get());
       expected = storage.get());
  storage = std::move(desired);
}

// idea: if we want anything to be updated on the GUI, you basically collect
// 1/60 s worth of data and send it all at once (rate limit sending info back
// to match refresh rate)

// Napi::Number add_module(const Napi::CallbackInfo &info) {
//   // init a new module and return its id (index)
//   // if ("__OSCILLATOR_MODULE")
//   // topo sort vector?
// }

// void remove_module(const Napi::CallbackInfo &info) {
//   // topo sort vector?
// }

// void add_patch(const Napi::CallbackInfo &info) {
//   // module 1 to 2
// }

// void remove_patch(const Napi::CallbackInfo &info) {
//   // module 1 to 2
// }

// Napi::Number get_param(const Napi::CallbackInfo &info) {
//   // modify userData
// }

// void set_param(const Napi::CallbackInfo &info) {
//   auto new_coeffs = std::make_unique<>(new_coeffs);
//   for (auto *expected = storage.get();
//        !coeffs.compare_exchange_weak(expected, new_coeffs.get());
//        expected = storage.get()) {
//     storage = std::move(new_coeffs);
//   }
// }

Napi::Object Init(Napi::Env env, Napi::Object exports) {
  // TODO: define functions as lambdas in here with closure context __ out of scope?

  exports.Set(Napi::String::New(env, "startStream"), Napi::Function::New(env, StartStream));
  exports.Set(Napi::String::New(env, "stopStream"), Napi::Function::New(env, StopStream));

  return exports;
}

// TODO: not right
NODE_API_MODULE(NODE_GYP_MODULE_NAME, Init)
