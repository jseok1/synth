#ifndef MODULE_HPP
#define MODULE_HPP

class Module {
 public:
  Module(double freq_sample);
  virtual ~Module();
  
  virtual void process() = 0;

 protected:
  double freq_sample;
};

#endif
