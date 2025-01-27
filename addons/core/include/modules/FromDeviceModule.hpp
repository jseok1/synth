#ifndef FROM_DEVICE_MODULE
#define FROM_DEVICE_MODULE

#include <unordered_map>

#include "modules/Module.hpp"

class FromDeviceModule : public Module {
 public:
  enum FromDeviceParam : int {
  };
  enum FromDeviceInPort : int {
  };
  enum FromDeviceOutPort : int {
  };

  FromDeviceModule(double freq_sample);

  void process() override;
};

#endif
