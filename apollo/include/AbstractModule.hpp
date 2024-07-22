#ifndef ABSTRACT_MODULE_HPP
#define ABSTRACT_MODULE_HPP

class AbstractModule {
 public:
  AbstractModule(double freq_sample);
  virtual ~AbstractModule();
  virtual void process() = 0;

 protected:
  double freq_sample;
};

#endif
