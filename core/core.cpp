#include <napi.h>

#include <chrono>
#include <cmath>
#include <iostream>
#include <thread>

#include "OscillatorModule.hpp"
#include "Rack.hpp"
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

void StartStream(const Napi::CallbackInfo &args) {
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

    std::cout << "Starting stream..." << '\n';
    while ((err = Pa_IsStreamActive(stream)) == 1) {
      Pa_Sleep(100);
    }
    if (err != paNoError) {
      Pa_Terminate();
      std::cout << Pa_GetErrorText(err) << '\n';
      return;
    }

    std::cout << "Ending stream..." << '\n';
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

void StopStream(const Napi::CallbackInfo &args) {
  userData.running = false;
}

// idea: if we want anything to be updated on the GUI, you basically collect
// 1/60 s worth of data and send it all at once (rate limit sending info back
// to match refresh rate)

void AddModule(const Napi::CallbackInfo &args) {
  Napi::Env env = args.Env();
  if (args.Length() != 2 || !args[0].IsNumber() || !args[1].IsNumber()) {
    Napi::TypeError::New(env, "Usage: addModule(moduleId: number, moduleType: number): void").ThrowAsJavaScriptException();
  }

  int module_id = args[0].As<Napi::Number>().Int32Value();
  int module_type = args[1].As<Napi::Number>().Int32Value();

  std::shared_ptr<Module> module;
  switch (module_type) {
    case 0: {
      module = std::make_shared<OscillatorModule>(FREQ_SAMPLE);
      break;
    }
    default: {
      Napi::TypeError::New(env, "moduleType is invalid.").ThrowAsJavaScriptException();
    }
  }

  userData.rack.add_module(module_id, module);
  userData.rack.sort_modules();
}

void RemoveModule(const Napi::CallbackInfo &args) {
  Napi::Env env = args.Env();
  if (args.Length() != 1 || !args[0].IsNumber()) {
    Napi::TypeError::New(env, "Usage: removeModule(moduleId: number): void").ThrowAsJavaScriptException();
  }

  int module_id = args[0].As<Napi::Number>().Int32Value();

  userData.rack.remove_module(module_id);
  userData.rack.sort_modules();
}

void UpdateModule(const Napi::CallbackInfo &args) {
  Napi::Env env = args.Env();
  if (args.Length() != 3 || !args[0].IsNumber() || !args[1].IsNumber() || !args[2].IsNumber()) {
    Napi::TypeError::New(env, "Usage: updateModule(moduleId: number, paramId: number, param: number): void").ThrowAsJavaScriptException();
  }

  int module_id = args[0].As<Napi::Number>().Int32Value();
  int param_id = args[1].As<Napi::Number>().Int32Value();
  double param = args[2].As<Napi::Number>().DoubleValue();

  userData.rack.update_module(module_id, param_id, param);
}

// TODO: make_unique and pass ownership
void AddCable(const Napi::CallbackInfo &args) {
  Napi::Env env = args.Env();
  if (args.Length() != 4 || !args[0].IsNumber() || !args[1].IsNumber() || !args[2].IsNumber() || !args[3].IsNumber()) {
    Napi::TypeError::New(env, "Usage: addCable(inModuleId: number, inPortId: number, outModuleId: number, outPortId: number): void").ThrowAsJavaScriptException();
  }

  int in_module_id = args[0].As<Napi::Number>().Int32Value();
  int in_port_id = args[1].As<Napi::Number>().Int32Value();
  int out_module_id = args[2].As<Napi::Number>().Int32Value();
  int out_port_id = args[3].As<Napi::Number>().Int32Value();

  std::shared_ptr<Cable> cable = std::make_shared<Cable>(out_module_id, out_port_id);

  userData.rack.add_cable(in_module_id, in_port_id, cable);
  userData.rack.sort_modules();
}

void RemoveCable(const Napi::CallbackInfo &args) {
  Napi::Env env = args.Env();
  if (args.Length() != 2 || !args[0].IsNumber() || !args[1].IsNumber()) {
    Napi::TypeError::New(env, "Usage: removeCable(inModuleId: number, inPortId: number): void").ThrowAsJavaScriptException();
  }

  int in_module_id = args[0].As<Napi::Number>().Int32Value();
  int in_port_id = args[1].As<Napi::Number>().Int32Value();

  userData.rack.remove_cable(in_module_id, in_port_id);
  userData.rack.sort_modules();
}

Napi::Object Init(Napi::Env env, Napi::Object exports) {
  // TODO: define functions as lambdas in here with closure context __ out of scope?

  exports.Set(Napi::String::New(env, "startStream"), Napi::Function::New(env, StartStream));
  exports.Set(Napi::String::New(env, "stopStream"), Napi::Function::New(env, StopStream));
  exports.Set(Napi::String::New(env, "addModule"), Napi::Function::New(env, AddModule));
  exports.Set(Napi::String::New(env, "removeModule"), Napi::Function::New(env, RemoveModule));
  exports.Set(Napi::String::New(env, "updateModule"), Napi::Function::New(env, UpdateModule));
  exports.Set(Napi::String::New(env, "addCable"), Napi::Function::New(env, AddCable));
  exports.Set(Napi::String::New(env, "removeCable"), Napi::Function::New(env, RemoveCable));

  return exports;
}

NODE_API_MODULE(PROJECT_NAME, Init)
