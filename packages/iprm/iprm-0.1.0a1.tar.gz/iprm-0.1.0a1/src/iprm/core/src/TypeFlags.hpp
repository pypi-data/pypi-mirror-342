/*
 * Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>
 *
 * SPDX-License-Identifier: MIT
 */
#pragma once

#include <cstdint>
#include <type_traits>

namespace iprm {

enum class TypeFlags : std::int64_t {
  NONE = 0LL,
  PROJECT = 1LL << 0,
  SUBDIR = 1LL << 1,
  TARGET = 1LL << 2,
  TEST = 1LL << 3,
  EXECUTABLE = 1LL << 4,
  LIBRARY = 1LL << 5,
  HEADER = 1LL << 6,
  STATIC = 1LL << 7,
  SHARED = 1LL << 8,
  GUI = 1LL << 9,
  THIRDPARTY = 1LL << 10,
  IMPORTED = 1LL << 11,
  PKGCONFIG = 1LL << 12,
  ARCHIVE = 1LL << 13,
  SOURCE = 1LL << 14,
  PRECOMPILED = 1LL << 15,
  GIT = 1LL << 16,
  VCPKG = 1LL << 17,
  CONAN = 1LL << 18,
  HOMEBREW = 1LL << 19,
  SYSTEM = 1LL << 20,
  DPKG = 1LL << 21,
  RPM = 1LL << 22,
  CONTAINER = 1LL << 23,
  CRTSTATIC = 1LL << 24,
  CRTDYNAMIC = 1LL << 25,
  CPP = 1LL << 26,
  RUST = 1LL << 27,
  PYTHON = 1LL << 28,
  QT = 1LL << 29,
  MSVC = 1LL << 30,
  CLANG = 1LL << 31,
  GCC = 1LL << 32,
  EMSCRIPTEN = 1LL << 33,
  RUSTC = 1LL << 34
};

inline TypeFlags operator|(TypeFlags a, TypeFlags b) {
  return static_cast<TypeFlags>(
      static_cast<std::underlying_type_t<TypeFlags>>(a) |
      static_cast<std::underlying_type_t<TypeFlags>>(b));
}

inline TypeFlags operator&(TypeFlags a, TypeFlags b) {
  return static_cast<TypeFlags>(
      static_cast<std::underlying_type_t<TypeFlags>>(a) &
      static_cast<std::underlying_type_t<TypeFlags>>(b));
}

inline TypeFlags operator~(TypeFlags a) {
  return static_cast<TypeFlags>(
      ~static_cast<std::underlying_type_t<TypeFlags>>(a));
}

}  // namespace iprm
