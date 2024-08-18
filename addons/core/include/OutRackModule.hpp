#ifndef OUT_RACK_MODULE
#define OUT_RACK_MODULE

#include <unordered_map>

#include "Module.hpp"

class OutRackModule : public Module {
 public:
  enum OutRackModuleInPort : int {
    in_t
  };

  OutRackModule(double freq_sample);

  void process() override;
};

#endif
