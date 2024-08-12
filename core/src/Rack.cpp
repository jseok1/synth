#include "Rack.hpp"

#include <iostream>
#include <memory>
#include <unordered_map>
#include <unordered_set>
#include <vector>

Rack::Rack() : sorted_module_ids{}, modules{}, cables{} {}

double Rack::process() {
  for (auto in_module_id : sorted_module_ids) {
    const auto &in_module = modules[in_module_id];
    for (auto &[in_port_id, in_port] : in_module->in_ports) {
      const auto &cable = cables[in_module_id][in_port_id];
      if (cable) {
        auto out_module_id = cable->module_id;
        auto out_port_id = cable->out_port_id;
        const auto &out_port = modules[out_module_id]->out_ports[out_port_id];

        in_port.volt = out_port.volt;
      }
    }

    modules[in_module_id]->process();
  }
  // some sort of fixed output module
  return 0.0;
}

void Rack::add_module(int module_id, std::shared_ptr<Module> module) {
  remove_module(module_id);
  modules.insert({module_id, module});
}

void Rack::remove_module(int module_id) {
  modules.erase(module_id);

  for (const auto &[in_module_id, in_module] : modules) {
    for (auto &[in_port_id, in_port] : in_module->in_ports) {
      const auto &cable = cables[in_module_id][in_port_id];
      if (cable) {
        auto out_module_id = cable->module_id;

        if (out_module_id == module_id) {
          remove_cable(in_module_id, in_port_id);
        }
      }
    }
  }
}

void Rack::update_module(int module_id, int param_id, double param) {
  modules[module_id]->params[param_id] = param;
}

void Rack::add_cable(int in_module_id, int in_port_id, std::shared_ptr<Cable> cable) {
  remove_cable(in_module_id, in_port_id);
  cables[in_module_id].insert({in_port_id, cable});

  modules[in_module_id]->in_ports[in_port_id].is_connected = true;
}

void Rack::remove_cable(int in_module_id, int in_port_id) {
  cables[in_module_id].erase(in_port_id);

  if (!cables[in_module_id].size()) {
    cables.erase(in_module_id);
  }

  modules[in_module_id]->in_ports[in_port_id].volt = 0.0;
  modules[in_module_id]->in_ports[in_port_id].is_connected = false;
}

void Rack::sort_modules() {
  sorted_module_ids.clear();

  std::unordered_set<int> visited_module_ids{};

  for (const auto &[in_module_id, in_module] : modules) {
    if (!visited_module_ids.count(in_module_id)) {
      sort_modules(in_module_id, visited_module_ids);
    }
  }

  std::cout << "Sorted: ";
  for (auto module_id : sorted_module_ids) {
    std::cout << module_id << ' ';
  }
  std::cout << '\n';
}

void Rack::sort_modules(int in_module_id, std::unordered_set<int> &visited_module_ids) {
  visited_module_ids.insert(in_module_id);

  const auto &in_module = modules[in_module_id];
  for (const auto &[in_port_id, in_port] : in_module->in_ports) {
    const auto &cable = cables[in_module_id][in_port_id];
    if (cable) {
      auto out_module_id = cable->module_id;

      if (!visited_module_ids.count(out_module_id)) {
        sort_modules(out_module_id, visited_module_ids);
      }
    }
  }

  sorted_module_ids.push_back(in_module_id);
}
