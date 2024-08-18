#ifndef RACK_HPP
#define RACK_HPP

#include <memory>
#include <unordered_map>
#include <unordered_set>
#include <vector>

#include "Module.hpp"

struct Cable {
  int module_id;
  int out_port_id;
};

class Rack {
 public:
  Rack();

  double process();
  void add_module(int module_id, std::shared_ptr<Module> module);
  void remove_module(int module_id);
  void update_module(int module_id, int param_id, double param);
  void add_cable(int in_module_id, int in_port_id, std::shared_ptr<Cable> cable);
  void remove_cable(int in_module_id, int in_port_id);
  void sort_modules();

 private:
  std::vector<int> sorted_module_ids;
  std::unordered_map<int, std::shared_ptr<Module>> modules;
  std::unordered_map<int, std::unordered_map<int, std::shared_ptr<Cable>>> cables;

  void sort_modules(int in_module_id, std::unordered_set<int> &visited_module_ids);
};

#endif

// can I queue updates which get consumed before process is called?
// probably but every heap allocation will have to be done before queuing
// instead of event handling, frontend should sample status at a determined frequency
// then this can read it
// or a rate divided event handler also work if fast enough?
