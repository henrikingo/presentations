# "Guest" Speaker Series on Performance

## MongoDB, 2019-05-19

Julian Edwards, Henrik Ingo, Eric Milkie

-----

# Agenda

- What is performance, anyway?
- "Profiler" is a kind of "tool"
- Demos
  - Julian Edwards: perf & FlameGraphs
  - Henrik Ingo: gdb & calltree.py
  - Eric Milkie: Intel VTune

-----

# Correctness

* Correctness is binary:
  * Given input => output
  * Must not crash
  * Any deviation is FAIL
  * Failures can be reproduced and debugged in 1-3 threads

-----
# Performance

* Better / worse. NOT binary.
* Holistic: What is total output of all threads?
* Profiling:
  * Where does a thread spend time over its lifecycle?
  * Where does the system spend time, aggregated over all threads?

-----
# Optimization question

Last month I spent $450 on Starbucks & $50 on champagne.

*What can I do to save money?*

This is profiling!

-----
# All the tools

* Evergreen
* Build
* Deploy
* Test (or Prod)
* Metrics
* BF (or SFDC) ticket
* Profiling
* SERVER ticket
* git commit


-----
# T2


-----
# Demo

