# Developer Tools - Queues

Python package containing modules implementing queue-like data
structures.

- **Repositories**
  - [dtools.queues][1] project on *PyPI*
  - [Source code][2] on *GitHub*
- **Detailed documentation**
  - [Detailed API documentation][3] on *GH-Pages*

This project is part of the [Developer Tools for Python][4] **dtools.**
namespace project.

## Overview

Queue-based data structures allowing developers to focus on the
algorithms they are using instead of all the "bit fiddling" required to
implement behaviors, perform memory management, and handle coding edge
cases.

### Module dtools.queues.types

These queues limit the developer to certain types of data access and are
geared to specific algorithmic use cases.

They allow iterators to leisurely iterate over inaccessible copies of
internal state while the data structures themselves are free to safely
mutate. They are designed to be reasonably "atomic" without introducing
inordinate complexity.

- *module* dtools.queues.types
  - *class* FIFOQueue: First-In-First-Out Queue
  - *class* LIFOQueue: Last-In-First-Out Queue
  - *class* DoubleQueue: Double-Sided Queue

Sometimes the real power of a data structure comes not from what it
empowers you to do, but from what it prevents you from doing to
yourself.

[1]: https://pypi.org/project/dtools.queues/
[2]: https://github.com/grscheller/dtools-queues/
[3]: https://grscheller.github.io/dtools-docs/queues/
[4]: https://github.com/grscheller/dtools-docs
