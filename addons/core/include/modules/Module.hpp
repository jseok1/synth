#ifndef MODULE_HPP
#define MODULE_HPP

#include <chrono>
#include <memory>
#include <unordered_map>

#include "Port.hpp"
// 1 - IDs. Cables managed by Synth. Just use a set of edges. Runtime wouldn't be the best.
// But simple. Also Module/Ports don't need to know about their IDs.
// NEED to copy volt. AND zero out from Synth.
// 2 - Shared pointer to module in cable. Don't need to copy volt over.
// Cables sorted in topo order?

class Module {
 public:
  std::unordered_map<int, double> params;  // wrap <, <double>>
  std::unordered_map<int, InPort> in_ports;
  std::unordered_map<int, OutPort> out_ports;

  Module(
    double freq_sample,
    std::unordered_map<int, double> params,
    std::unordered_map<int, InPort> in_ports,
    std::unordered_map<int, OutPort> out_ports
  );
  virtual ~Module();

  virtual void process() = 0;
  std::chrono::high_resolution_clock::time_point start;

 protected:
  const double freq_sample;
};

#endif

// struct Cable {
//   int module_id;
//   int out_port_id;
// };

// struct InPort {
//   double volt;
//   Cable cable;
// };

// struct OutPort {
//   double volt;
// };

// struct Cable {
//   std::weak_ptr<Module> module;
//   int out_port_id;
// };

// struct InPort {
//   Cable cable;

//   double volt();
//   bool is_connected();
// };

// struct OutPort {
//   double volt;
// };

// ^ but then you'd need module_id to mark as visited.
// you either need module_id in the module itself or the cable.
// both would be redundant
