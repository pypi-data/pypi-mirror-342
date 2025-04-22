/*
 * Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>
 *
 * SPDX-License-Identifier: MIT
 */
#pragma once

#include "../util/APIBridge.hpp"
#include "FileSystemModel.hpp"

#include <QTreeView>

#include <filesystem>

namespace iprm {

class FileSystemView : public QTreeView {
  Q_OBJECT

 public:
  explicit FileSystemView(QWidget* parent = nullptr);

  void track_builtins(const QList<SystemBackend>& builtins);
  void track_plugins(const QList<SystemBackend>& plugins);

  void select_file(const std::filesystem::path& file_path);

  void load_tree(const std::string& native_file_name,
                 const std::vector<std::filesystem::path>& files,
                 const std::filesystem::path& root_dir);

  void reload_tree();

 Q_SIGNALS:
  void file_activated(const FileNode& file_node);

 private Q_SLOTS:
  void on_activated(const QModelIndex& index);

 private:
  QModelIndex find_index(const QModelIndex& parent_index,
                         const std::filesystem::path& target_path);

  FileSystemModel* fs_model_{nullptr};
  FileSystemSortFilterProxyModel* fs_proxy_model_{nullptr};
};

}  // namespace iprm
