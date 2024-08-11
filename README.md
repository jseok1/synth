# TODO
* Reimplement VCO using wavetables to mimic analog.
* Reimplement VCF using digital Moog ladder filter to mimic analog.
* Rename volt_per_oct_t.
* Implement keyboard tracking for VCF.
* Reverb.
* Delay.
* Noise.
* LFO.
* Fix modulation and think about VCA amp_t vs amp_mod_t.
* Better separation of C++ and JS.
* Look into CMake.js instead of node-gyp?

# Useful Resources
https://www.earlevel.com/main/
https://dsp.stackexchange.com/questions/2555/help-with-equations-for-exponential-adsr-envelope
https://github.com/PortAudio/portaudio/wiki/Tips_Callbacks
https://portaudio.music.columbia.narkive.com/aBz3Ymnk/postponing-callback-during-critical-sections
https://stackoverflow.com/questions/57206197/lockless-circular-buffer-with-single-producer-singular-consumer
https://stackoverflow.com/questions/14142023/why-is-a-single-producer-single-consumer-circular-queue-thread-safe-without-lock
https://portaudio.music.columbia.narkive.com/snc4IQsB/multithreading-and-mutexes
https://www.youtube.com/watch?v=Q0vrQFyAdWI
https://www.youtube.com/watch?v=PoZAo2Vikbo


# Graph Structure
Modules and ports with cables form a DAG.
Modules may have multiple edges going to another module.
Input ports can have at most one cable, thus uniquely identify cables.
Output ports may have more than one cable.
A topological sort of a DAG is the reversed topological sort of the reversed DAG.
Modules are vertices. Ports identify edges.
