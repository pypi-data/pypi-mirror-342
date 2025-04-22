/*
 * Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>
 *
 * SPDX-License-Identifier: MIT
 */
#include "Session.hpp"
#include "Object.hpp"

namespace iprm {
std::unique_ptr<Session> Session::instance_;

Session::Session(const std::string& root_dir) : root_dir_(root_dir) {}

void Session::create(const std::string& root_dir) {
  instance_ = std::make_unique<Session>(root_dir);
}

void Session::destroy() {
  instance_.reset(nullptr);
}

void Session::register_object(const std::shared_ptr<Object>& obj) {
  instance_->register_object_impl(obj);
}

void Session::begin_platform_context(const std::string& platform) {
  instance_->begin_platform_context_impl(platform);
}

void Session::end_platform_context() {
  instance_->end_platform_context_impl();
}

void Session::begin_file_context(const std::string& entry_file_path) {
  instance_->begin_file_context_impl(entry_file_path);
}

void Session::end_file_context() {
  instance_->end_file_context_impl();
}

std::shared_ptr<Object> Session::get_object(const std::string& obj_name) {
  return instance_->get_object_impl(obj_name);
}

std::unordered_map<std::string, std::vector<std::shared_ptr<Object> > >
Session::get_objects() {
  return instance_->get_objects_impl();
}

void Session::register_rename(const std::string& new_name,
                              const std::shared_ptr<Object>& stale_obj) {
  instance_->register_rename_impl(new_name, stale_obj);
}

std::vector<std::string> Session::retrieve_loadable_files() {
  return instance_->retrieve_loadable_files_impl();
}

std::string Session::root_relative_source_dir() {
  return instance_->root_relative_source_dir_impl();
}

void Session::register_object_impl(const std::shared_ptr<Object>& obj) {
  if (!action_platform_ctx_.has_value() || !active_file_ctx_.has_value()) {
    // TODO: We should log something out to the active log sink
    //  (a handle to this sink should be optionally passed in for the
    //  environment dict)
    return;
  }
  objects_[action_platform_ctx_.value()][active_file_ctx_.value().string()]
      .push_back(obj);
}

void Session::begin_platform_context_impl(const std::string& platform) {
  action_platform_ctx_ = platform;
}

void Session::end_platform_context_impl() {
  action_platform_ctx_.reset();
}

void Session::begin_file_context_impl(const std::string& entry_file_path) {
  active_file_ctx_ = std::filesystem::path{entry_file_path};
}

void Session::end_file_context_impl() {
  active_file_ctx_.reset();
}

std::shared_ptr<Object> Session::get_object_impl(
    const std::string& obj_name) const {
  auto platform_objects = active_platform_objects_impl();
  if (!platform_objects.has_value()) {
    return nullptr;
  }

  for (const auto& [file_path, objects] : platform_objects.value().get()) {
    for (const auto& obj : objects) {
      if (obj->name() == obj_name) {
        // Need to create a new shared_ptr since we only store references
        return obj;
      }
    }
  }
  return nullptr;
}

std::unordered_map<std::string, std::vector<std::shared_ptr<Object>>>
Session::get_objects_impl() const {
  auto platform_objects = active_platform_objects_impl();
  if (!platform_objects.has_value()) {
    return {};
  }
  return platform_objects.value().get();
}

// TODO: This can/should be removed, the initial design perform implicit
//  renaming which is not a thing anymore
void Session::register_rename_impl(const std::string& new_name,
                                   const std::shared_ptr<Object>& stale_obj) {
  auto platform_objects = active_platform_objects_impl();
  if (!platform_objects.has_value()) {
    return;
  }

  const std::string old_name = stale_obj->name();

  // Update the name in all relevant objects
  for (auto& [file_path, objects] : platform_objects.value().get()) {
    for (auto& obj : objects) {
      if (obj->name() == old_name) {
        obj->set_name(new_name);
        break;
      }
    }
  }
}

std::vector<std::string> Session::retrieve_loadable_files_impl() const {
  std::vector<std::string> loadable_file_paths;
  for (const auto& entry :
       std::filesystem::recursive_directory_iterator(root_dir_)) {
    if (entry.path().filename() == FILE_NAME) {
      const auto& entry_path = entry.path();
      loadable_file_paths.push_back(entry_path.generic_string());
    }
  }
  return loadable_file_paths;
}

std::string Session::root_relative_source_dir_impl() const {
  // TODO: We should return a 'None' in the case there is no active file context
  const auto active_file_ctx_dir_path =
      active_file_ctx_.has_value() ? active_file_ctx_.value().parent_path()
                                   : "";
  const auto root_relative_dir_path =
      proximate(active_file_ctx_dir_path, root_dir_);
  // Use "Unix"-like path separators
  return root_relative_dir_path.generic_string();
}

std::optional<std::reference_wrapper<Session::platform_objects>>
Session::active_platform_objects_impl() const {
  if (!action_platform_ctx_.has_value()) {
    return std::nullopt;
  }

  auto platform_objects_itr = objects_.find(action_platform_ctx_.value());
  if (platform_objects_itr == objects_.end()) {
    return std::nullopt;
  }

  return std::ref(platform_objects_itr->second);
}

}  // namespace iprm
