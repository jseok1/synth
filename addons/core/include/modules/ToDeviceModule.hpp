#ifndef TO_DEVICE_MODULE
#define TO_DEVICE_MODULE

#include <unordered_map>

#include "modules/Module.hpp"

class ToDeviceModule : public Module {
 public:
  enum ToDeviceParam : int {
  };
  enum ToDeviceInPort : int {
    __IN
  };
  enum ToDeviceOutPort : int {
  };

  ToDeviceModule(double freq_sample);

  void process() override;
};

#endif
