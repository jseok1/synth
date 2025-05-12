#pragma once

enum IO {
  __IN,
  __OUT
}

struct InPort {
  double volt;
  bool is_connected;  // or replace with cable-id
};

struct OutPort {
  double volt;
  // list of cable ids
};

// union of enums possible in C++?

