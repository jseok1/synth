#include <napi.h>
#include <portaudio.h>

#include <chrono>
#include <cmath>
#include <iostream>
#include <thread>

#include "Rack.hpp"
#include "modules/AmplifierModule.hpp"
#include "modules/EnvelopeModule.hpp"
#include "modules/FilterModule.hpp"
#include "modules/FromDeviceModule.hpp"
#include "modules/MixerModule.hpp"
#include "modules/OscillatorModule.hpp"
#include "modules/ToDeviceModule.hpp"

enum ModuleType : int {
  __TO_DEVICE,
  __FROM_DEVICE,
  __OSCILLATOR,
  __ENVELOPE,
  __FILTER,
  __AMPLIFIER,
  __MIXER
};

const double freq_sample = 44100;
const unsigned long sample_size = 256;

struct PaUserData {
  Rack rack;
  bool is_running = false;
  long tick = 0;
} userData;

// could be a lambda
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

  for (unsigned long i = 0; i < sample_size; i++) {
    *out++ = data->rack.process();
  }

  // auto stop = chrono::high_resolution_clock::now();
  if (data->tick % 100 == 0) {
    // auto duration = chrono::duration_cast<chrono::microseconds>(stop - start);
    // std::cout << duration.count() << '\n';
  }
  data->tick++;

  int flag =
    data->is_running ? PaStreamCallbackResult::paContinue : PaStreamCallbackResult::paComplete;
  return flag;
}

void StartStream(const Napi::CallbackInfo &args) {
  // if there's already an audio thread, don't spawn another one
  if (userData.is_running) return;

  // TODO: need more robust guards --> is a thread created/being created?
  userData.is_running = true;

  auto main = []() {
    PaError err{};

    err = Pa_Initialize();
    if (err != paNoError) {
      std::cout << Pa_GetErrorText(err) << '\n';
      return;
    }

    PaStream *stream;
    PaStreamParameters outputParameters;
    outputParameters.device = Pa_GetDefaultOutputDevice();
    outputParameters.channelCount = 1;
    outputParameters.sampleFormat = paFloat32;
    outputParameters.suggestedLatency =
      Pa_GetDeviceInfo(outputParameters.device)->defaultLowOutputLatency;
    outputParameters.hostApiSpecificStreamInfo = NULL;

    std::cout << "Suggested latency: " << outputParameters.suggestedLatency << std::endl;
    err = Pa_OpenStream(
      &stream,
      NULL,
      &outputParameters,
      freq_sample,
      sample_size,
      paClipOff,
      streamCallback,
      &userData
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

    std::cout << "Stoping stream..." << '\n';
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
  userData.is_running = false;
}

// idea: if we want anything to be updated on the GUI, you basically collect
// 1/60 s worth of data and send it all at once (rate limit sending info back
// to match refresh rate)

void AddModule(const Napi::CallbackInfo &args) {
  Napi::Env env = args.Env();
  if (args.Length() != 2 || !args[0].IsNumber() || !args[1].IsNumber()) {
    Napi::TypeError::New(env, "Usage: addModule(moduleId: number, moduleType: number): void")
      .ThrowAsJavaScriptException();
  }

  int module_id = args[0].As<Napi::Number>().Int32Value();
  int module_type = args[1].As<Napi::Number>().Int32Value();

  std::shared_ptr<Module> module;
  switch (module_type) {
    case ModuleType::__TO_DEVICE: {
      module = std::make_shared<ToDeviceModule>(freq_sample);
      break;
    }
    case ModuleType::__FROM_DEVICE: {
      module = std::make_shared<FromDeviceModule>(freq_sample);
      break;
    }
    case ModuleType::__OSCILLATOR: {
      module = std::make_shared<OscillatorModule>(freq_sample);
      break;
    }
    case ModuleType::__ENVELOPE: {
      module = std::make_shared<EnvelopeModule>(freq_sample);
      break;
    }
    case ModuleType::__FILTER: {
      module = std::make_shared<FilterModule>(freq_sample);
      break;
    }
    case ModuleType::__AMPLIFIER: {
      module = std::make_shared<AmplifierModule>(freq_sample);
      break;
    }
    case ModuleType::__MIXER: {
      module = std::make_shared<MixerModule>(freq_sample);
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
    Napi::TypeError::New(env, "Usage: removeModule(moduleId: number): void")
      .ThrowAsJavaScriptException();
  }

  int module_id = args[0].As<Napi::Number>().Int32Value();

  userData.rack.remove_module(module_id);
  userData.rack.sort_modules();
}

void UpdateParam(const Napi::CallbackInfo &args) {
  Napi::Env env = args.Env();
  if (args.Length() != 3 || !args[0].IsNumber() || !args[1].IsNumber() || !args[2].IsNumber()) {
    Napi::TypeError::New(
      env, "Usage: updateParam(moduleId: number, paramId: number, param: number): void"
    )
      .ThrowAsJavaScriptException();
  }

  int module_id = args[0].As<Napi::Number>().Int32Value();
  int param_id = args[1].As<Napi::Number>().Int32Value();
  double param = args[2].As<Napi::Number>().DoubleValue();

  userData.rack.update_param(module_id, param_id, param);
}

// TODO: make_unique and pass ownership
void AddCable(const Napi::CallbackInfo &args) {
  Napi::Env env = args.Env();
  if (args.Length() != 4 || !args[0].IsNumber() || !args[1].IsNumber() || !args[2].IsNumber() ||
      !args[3].IsNumber()) {
    Napi::TypeError::New(
      env,
      "Usage: addCable(inModuleId: number, inPortId: number, outModuleId: number, outPortId: "
      "number): void"
    )
      .ThrowAsJavaScriptException();
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
    Napi::TypeError::New(env, "Usage: removeCable(inModuleId: number, inPortId: number): void")
      .ThrowAsJavaScriptException();
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
  exports.Set(Napi::String::New(env, "updateParam"), Napi::Function::New(env, UpdateParam));
  exports.Set(Napi::String::New(env, "addCable"), Napi::Function::New(env, AddCable));
  exports.Set(Napi::String::New(env, "removeCable"), Napi::Function::New(env, RemoveCable));

  return exports;
}

NODE_API_MODULE(PROJECT_NAME, Init)
