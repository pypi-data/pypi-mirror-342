# Developer Tools - Queues

Python package containing modules implementing queue-like data
structures.

- **Repositories**
  - [dtools.splitends][1] project on *PyPI*
  - [Source code][2] on *GitHub*
- **Detailed documentation**
  - [Detailed API documentation][3] on *GH-Pages*

This project is part of the [Developer Tools for Python][4] **dtools.**
namespace project.

## Package dtools.splitends

Singularly linked data structures allowing data to be safely shared
between multiple instances by making shared data immutable and
inaccessible to client code.

- *module* dtools.splitends.splitend`
  - *class* SplitEnd: Singularly link stack with shareable data nodes
- *module* dtools.splitends.splitend_node
  - *class* SENode: node class used by class SplitEnd 

______________________________________________________________________

[1]: https://pypi.org/project/dtools.splitends/
[2]: https://github.com/grscheller/dtools-splitends/
[3]: https://grscheller.github.io/dtools-docs/splitends/
[4]: https://github.com/grscheller/dtools-docs
