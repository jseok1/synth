#include <napi.h>

#include <cmath>
#include <iostream>
#include <thread>
#include <chrono>

#include "Rack.h"
#include "portaudio.h"

#define FREQ_SAMPLE 44100
#define SAMPLE_SIZE 256

struct PaUserData {
  Rack rack;
  bool running;
  long tick;
} userData;

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

  // auto start = chrono::high_resolution_clock::now();

  PaUserData *data = (PaUserData *)userData;
  float *out = (float *)outputBuffer;

  for (unsigned long i = 0; i < SAMPLE_SIZE; i++) {
    *out++ = data->rack.process();
  }

  // auto stop = chrono::high_resolution_clock::now();
  if (data->tick % 100 == 0) {
    // auto duration = chrono::duration_cast<chrono::microseconds>(stop - start);
    // std::cout << duration.count() << '\n';
  }
  data->tick++;

  int flag =
    data->running ? PaStreamCallbackResult::paContinue : PaStreamCallbackResult::paComplete;
  return flag;
}

void start_stream(const Napi::CallbackInfo &info) {
  auto main = []() {
    PaError err{};

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

void stop_stream(const Napi::CallbackInfo &info) {
  userData.running = false;
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

  exports.Set(Napi::String::New(env, "startStream"), Napi::Function::New(env, start_stream));
  exports.Set(Napi::String::New(env, "stopStream"), Napi::Function::New(env, stop_stream));

  return exports;
}

// TODO: not right
NODE_API_MODULE(NODE_GYP_MODULE_NAME, Init)
