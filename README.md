# SynthSandbox [WIP]

## TODO

- Extract mapping of module types and port types into a single source of truth shared by JS and C++.
- Look into RCU for handling concurrency in real-time systems.
- Reimplement VCO using wavetables to mimic analog.
- Reimplement VCF using digital Moog ladder filter to mimic analog.
- Implement key tracking for VCF.
- Modules: LFO, sequencer, delay, reverb, noise.
- Add C++ performance logging.
- Change shared_ptr to unique_ptr.
- Think of a good name.
- Catenary curves for cables (interesting challenge: model Catenary curves using Bezier).
- Disallow self cable loops in frontend.
- Quantization module
- Drag to scroll

From a variable naming/thinking point of view, inModule vs. outModule is from the context of cables.

There are two entities managed by the rack: modules and cables.
From the React side, the creation and deletion of modules and cables are tied to component lifecycles, namely through effects (like RAII). Therefore, the React side never had to know anything about the logic of the application.

## Useful Resources

https://www.earlevel.com/main/
https://dsp.stackexchange.com/questions/2555/help-with-equations-for-exponential-adsr-envelope
https://github.com/PortAudio/portaudio/wiki/Tips_Callbacks
https://portaudio.music.columbia.narkive.com/aBz3Ymnk/postponing-callback-during-critical-sections
https://stackoverflow.com/questions/57206197/lockless-circular-buffer-with-single-producer-singular-consumer
https://stackoverflow.com/questions/14142023/why-is-a-single-producer-single-consumer-circular-queue-thread-safe-without-lock
https://portaudio.music.columbia.narkive.com/snc4IQsB/multithreading-and-mutexes
https://www.youtube.com/watch?v=Q0vrQFyAdWI
https://www.youtube.com/watch?v=PoZAo2Vikbo
https://stackoverflow.com/questions/23214614/time-between-callback-calls/23226247#23226247
https://stackoverflow.com/questions/21064101/understanding-offsetwidth-clientwidth-scrollwidth-and-height-respectively

## Graph Structure & Topological Sort

Modules and ports with cables form a DAG.
Modules may have multiple edges going to another module.
Input ports can have at most one cable, thus uniquely identify cables.
Output ports may have more than one cable.
A topological sort of a DAG is the reversed topological sort of the reversed DAG. Therefore, cables can be represented as directed edges from input ports to output ports.
Modules are vertices. Ports identify edges. There may be multiple edges from one vertex to another.
There can be multiple source vertices but only one destination vertex.

## Interval Sorting

The drag & drop functionality works by sorting modules by their top-left position. This is like
interval sorting. 

## React notes

When context changes, only components calling useContext will rerender.
When a parent component's state changes, its child components will rerender if they receive props,
even if the props don't change (unless memoized). However children that do not receive props do not
rerender.
Callback functions passed as props to child components will trigger unnecessary rerenders since the
function is recreated, even if it's definition is the same. So memoization won't work. So use
useCallback.
Also when components are dynamically created using someStateArray.map(), when that state array changes,
components that retain the same key won't rerender.
