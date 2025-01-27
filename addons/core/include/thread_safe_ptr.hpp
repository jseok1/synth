#ifndef RCU_HPP
#define RCU_HPP

#include <atomic>
#include <memory>

/**
 * A simplified RCU implementation for a single reader and a single writer.
 * Multiple calls to read() are NOT guaranteed to be
 *
 *
 * Idea: double buffer where read goes to read_index=0, write goes to write_index=1
 * producer writes to back buffer
 * consumer reads from front buffer
 * Once all readers are finished, writer swaps read_index and write_index atomically
 * Then new write_index copy is updated with the read_index copy (blocking all other writes)
 * std::atomic<int>
 *
 * Multiple readers, single writer.
 */

template <typename T>
class thread_safe_ptr {
 public:
  class thread_safe_read_ptr {
   public:
    thread_safe_read_ptr() {}
    ~thread_safe_read_ptr() {}

    const T& operator*() {
      return ptr.buffers[read_buffer_id];
    }

    const T* operator->() {
      return &ptr.buffers[read_buffer_id];
    }

   private:
    thread_safe_ptr& ptr;
  };

  class thread_safe_write_ptr {
   public:
    thread_safe_write_ptr() {};
    ~thread_safe_write_ptr() {
      // call parent object to swap when no readers
    };

    const T& operator*() {
      return ptr.buffers[ptr.read_buffer_id.load() ^ 1];
    };

    const T* operator->() {
      return &ptr.buffers[ptr.read_buffer_id.load() ^ 1];
    };

   private:
    thread_safe_ptr& ptr;
  };

  thread_safe_read_ptr read_lock() {
    return thread_safe_read_ptr(*this);
  }

  thread_safe_write_ptr write_lock() {
    return thread_safe_write_ptr(*this);
  }

 private:
  std::array<T, 2> buffers;
  std::atomic<int> read_buffer_id; // write_buffer_id
  std::atomic<int> readers_count;
  std::atomic<int> writers_count;  // should not go above 1

  void swap_buffers() {
    while (readers_count) {
      std::this_thread::yield();
    }

    // but there might be a reader here
    read_buffer_id.store(read_buffer_id ^ 1);
  }
};

#endif
