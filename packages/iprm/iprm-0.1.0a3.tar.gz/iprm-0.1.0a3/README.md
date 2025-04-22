# Intermediate Project Representation Model

<p style="text-align:center">
<img src="./src/iprm/studio/res/logos/iprm.svg" width="300" height="300" alt="IPRM Logo">
</p>

[![PyPI version](https://img.shields.io/pypi/v/iprm.svg)](https://pypi.org/project/iprm/)

IPRM is to C++ build systems what LLVM is to CPU architectures.
One key goal is not to be yet another competitor to existing software in this space (e.g. CMake, Meson, Ninja, MSBuild,
GNU Make, QMake, SCons), just like
how LLVM is not a competitor to x86-64, Aarch64, and risc-v64. Instead, the goal is to be project
model/build system agnostic, enabling developer accessibility to a wide array of project
models/build systems via a common unified format. The actual project model or build
system used under the hood is up to the developer, allowing for ease of migration to
different backends, or to evaluate which backend is the most ideal for ones situation/preferences.

Developers act as the "compiler frontend", describing their large/complex C++ software project
in the .iprm format. Where-as typically an actual program is required/desired to emit the
intermediate representation, IPRM is designed so developers can do this manually because the
IPRM file format is just a python file that exposes an API tailor-made for all the varying tools
and strategies needed to describe C++ projects. IPRM then takes those files and acts as
the "compiler backend", taking its intermediate format and emitting a specific project model or
build system that can actually do the work of configuring, building, testing, and installing
C++ based projects

Another key goal is to maximize system resource utilization/parallelization during the build. There is a general 
focus/effort to delay as much work as possible (primarily third party/external resource retrieval/configuration) 
to be done at build time. This ensures targets are built as soon as their own dependencies have been built instead 
of having a "pre-build" phase where content is fetched and prepared in serial. Projects that migrate to IPRM, 
even if their original project was using the same system, have the potential to see a significant decrease in 
overall build time (starting from a clean repository), depending on how third party content was handled in their 
previous build infrastructure.

<p style="text-align:center">
<img src="./docs/cpp_build_abstraction_flow.svg" width="300" height="300" alt="IPRM Logo">
</p>


## Getting Started

### [Build Instructions](docs/building.md)
### [Documentation](docs/README.md)
