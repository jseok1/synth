// #ifndef RCU_HPP
// #define RCU_HPP

// #include <atomic>
// #include <memory>

// /**
//  * A simplified RCU implementation for a single reader and a single writer.
//  * Multiple calls to read() are NOT guaranteed to be
//  */
// template <typename T>
// class RCU {
//  public:
//   std::shared_ptr<T> read() const { return std::atomic_load(&data); }
//   // return pointer, which you dereference, then prevent that from being modified
//   // until pointer goes out of scope


//   void write(const T& new_value) {
//     std::shared_ptr<T> desired = std::make_shared<T>(new_value);
//     auto *expected = storage.get();
//     while (!param.compare_exchange_weak(expected, desired.get())) {
//       // sleep
//     }
//     storage = std::move(desired);
//   }

//  private:
//   std::atomic<T*> flag;
//   std::shared_ptr<T> data;
// };

// #endif
