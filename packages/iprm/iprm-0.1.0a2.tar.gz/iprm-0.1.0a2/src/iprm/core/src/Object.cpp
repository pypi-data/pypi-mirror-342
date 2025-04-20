/*
 * Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>
 *
 * SPDX-License-Identifier: MIT
 */
#include "Object.hpp"
#include "Session.hpp"

#include <pybind11/pybind11.h>

#include <filesystem>

namespace iprm {
void Object::rename(const std::string& new_name) {
  Session::register_rename(new_name, shared_from_this());
}

bool Object::is_type(TypeFlags type_flags) const {
  return static_cast<bool>(this->type_flags() & type_flags);
}

bool Object::is_project() const {
  return is_type(TypeFlags::PROJECT);
}
bool Object::is_subdir() const {
  return is_type(TypeFlags::SUBDIR);
}

bool Object::is_target() const {
  return is_type(TypeFlags::TARGET);
}

bool Object::is_test() const {
  return is_type(TypeFlags::TEST);
}

bool Object::is_executable() const {
  return is_type(TypeFlags::EXECUTABLE);
}

bool Object::is_library() const {
  return is_type(TypeFlags::STATIC) || is_type(TypeFlags::SHARED);
}

bool Object::is_header() const {
  return is_type(TypeFlags::HEADER);
}

bool Object::is_static_library() const {
  return is_type(TypeFlags::STATIC);
}

bool Object::is_shared_library() const {
  return is_type(TypeFlags::SHARED);
}

bool Object::is_gui() const {
  return is_type(TypeFlags::GUI);
}

bool Object::is_third_party() const {
  return is_type(TypeFlags::THIRDPARTY);
}

bool Object::is_imported() const {
  return is_type(TypeFlags::IMPORTED);
}

bool Object::is_pkgconfig() const {
  return is_type(TypeFlags::PKGCONFIG);
}

bool Object::is_precompiled_archive() const {
  return is_type(TypeFlags::ARCHIVE) && is_type(TypeFlags::PRECOMPILED);
}

bool Object::is_source_archive() const {
  return is_type(TypeFlags::ARCHIVE) && is_type(TypeFlags::SOURCE);
}

bool Object::is_git() const {
  return is_type(TypeFlags::GIT);
}

bool Object::is_vcpkg() const {
  return is_type(TypeFlags::VCPKG);
}

bool Object::is_conan() const {
  return is_type(TypeFlags::CONAN);
}

bool Object::is_homebrew() const {
  return is_type(TypeFlags::HOMEBREW);
}

bool Object::is_system() const {
  return is_type(TypeFlags::SYSTEM);
}

bool Object::is_dpkg() const {
  return is_type(TypeFlags::DPKG);
}

bool Object::is_rpm() const {
  return is_type(TypeFlags::RPM);
}

bool Object::is_container() const {
  return is_type(TypeFlags::CONTAINER);
}

bool Object::is_static_crt() const {
  return is_type(TypeFlags::CRTSTATIC);
}

bool Object::is_dynamic_crt() const {
  return is_type(TypeFlags::CRTDYNAMIC);
}

bool Object::is_cpp() const {
  return is_type(TypeFlags::CPP);
}

bool Object::is_rust() const {
  return is_type(TypeFlags::RUST);
}

bool Object::is_python() const {
  return is_type(TypeFlags::PYTHON);
}

bool Object::is_qt() const {
  return is_type(TypeFlags::QT);
}

}  // namespace iprm
