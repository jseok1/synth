#ifndef PORT_HPP
#define PORT_HPP

struct InPort {
  double volt;
  bool is_connected; // or replace with cable-id
};

struct OutPort {
  double volt;
  // list of cable ids
};

#endif
