/*
 * Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>
 *
 * SPDX-License-Identifier: MIT
 */
#pragma once

#include "../filesystem/FileSystemModel.hpp"
#include "../util/APIBridge.hpp"
#include "FileView.hpp"

#include <QFileInfo>
#include <QHash>
#include <QItemSelection>
#include <QTabWidget>

#include <functional>
#include <optional>

class QTabWidget;

namespace iprm {

class Project : public QTabWidget {
  Q_OBJECT

 public:
  Project(QWidget* parent = nullptr);

  void set_project_dir(const QDir& dir);

  void set_host_platform(const QString& host_platform_display_name,
                         const QIcon& host_platform_icon) {
    host_platform_display_name_ = host_platform_display_name;
    host_platform_icon_ = host_platform_icon;
  }

  void add_platform(const QString& display_name,
                    const QIcon& icon,
                    const QHash<QString, QList<ObjectNode>>& objects);

  void add_file(const FileNode& file_node);

  FileView* current_file() const;

  void close_file(FileView* file);

 Q_SIGNALS:
  void file_closed(int num_files_opened);

  void file_modified(bool modified);

 private Q_SLOTS:
  void on_file_tab_closed(int tab_index);

  void on_file_tab_changed(int tab_index);

 private:
  QDir project_dir_;

  FileView* add_native(const QString& native_file_path);
  void add_backend(const BackendFile& file_node);

  QHash<QString, FileView*> open_files_;
  QString host_platform_display_name_;
  std::optional<std::reference_wrapper<const QIcon>> host_platform_icon_;
  QHash<QString, PlatformProject> platforms_;
};

}  // namespace iprm
