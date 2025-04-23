# Copyright 2023-2024 Geoffrey R. Scheller
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
### Developer Tools - Queue based data structures

These are modeled after Python builtins. The initializers take at most one
iterable while factory functions stand in for Python syntax.

- Mutable data structures geared to specific algorithmic use cases
  - *class* dtools.queues.types.FIFOQueue: First In First Out Queue
  - *class* dtools.queues.types.LIFOQueue: Last In First Out Queue
  - *class* dtools.queues.types.DoubleQueue: Double-ended Queue
- Factory functions
  - *function* dtools.queues.types.fifo_queue: Create FIFOQueue from values
  - *function* dtools.queues.types.lifo_queue: Create LIFOQueue from values
  - *function* dtools.queues.types.double_queue: Create DoubleQueue from values

"""

__version__ = '1.0.0'
__author__ = 'Geoffrey R. Scheller'
__copyright__ = 'Copyright (c) 2023-2025 Geoffrey R. Scheller'
__license__ = 'Apache License 2.0'
