/*
 * Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>
 *
 * SPDX-License-Identifier: MIT
 */
#include "Project.hpp"
#include "../util/AssetCache.hpp"
#include "../util/util.hpp"

#include <QFile>
#include <QFileInfo>
#include <QLabel>
#include <QPainter>
#include <QSvgRenderer>
#include <QTabBar>
#include <QVBoxLayout>

#include <complex>
#include <filesystem>

namespace iprm {

Project::Project(QWidget* parent) : QTabWidget(parent) {
  setTabPosition(North);
  setMovable(true);
  setTabsClosable(true);
  connect(this, &Project::tabCloseRequested, this,
          &Project::on_file_tab_closed);
  connect(this, &Project::currentChanged, this, &Project::on_file_tab_changed);
}

void Project::set_project_dir(const QDir& dir) {
  project_dir_ = dir;
  while (count() > 0) {
    auto file_node = qobject_cast<FileView*>(widget(0));
    removeTab(0);
    file_node->deleteLater();
  }
  open_files_.clear();
}

void Project::add_platform(const QString& display_name,
                           const QIcon& icon,
                           const QHash<QString, QList<ObjectNode>>& objects) {
  QHash<QString, PlatformFile> files;
  QHashIterator project(objects);
  while (project.hasNext()) {
    project.next();
    const auto& file_path = project.key();
    const auto& file_objects = project.value();
    files.insert(file_path, PlatformFile{file_objects, icon});
  }
  platforms_.insert(display_name, PlatformProject{files});
}

void Project::add_file(const FileNode& file_node) {
  std::visit(overloaded{[](const Folder&) {
                          // Ignore Folders
                        },
                        [this](const NativeFile& n) {
                          const auto native_file_path =
                              QDir::toNativeSeparators(
                                  QString::fromStdString(n.path.string()));
                          (void)add_native(native_file_path);
                        },
                        [this](const BackendFile& n) { add_backend(n); }},
             file_node);
}

FileView* Project::add_native(const QString& native_file_path) {
  auto file_node_itr = open_files_.find(native_file_path);
  if (file_node_itr != open_files_.end()) {
    FileView* file_node = file_node_itr.value();
    setCurrentWidget(file_node);
    return file_node;
  }
  QFile native_file(native_file_path);
  if (!native_file.open(QIODevice::ReadOnly | QIODevice::Text)) {
    return nullptr;
  }

  QHash<QString, PlatformFile> file;
  QHashIterator platforms_itr(platforms_);
  while (platforms_itr.hasNext()) {
    platforms_itr.next();
    const auto& platform = platforms_itr.key();
    const auto& platform_files = platforms_itr.value().files_;
    const auto platform_file_itr = platform_files.find(native_file_path);
    if (platform_file_itr != platform_files.end()) {
      const auto& platform_file = platform_file_itr.value();
      file.emplace(platform, platform_file.objects_, platform_file.icon_);
    }
  }

  QFileInfo native_info(native_file.fileName());
  const QString native_file_name = native_info.fileName();
  const QString proj_relative_dir_path =
      project_dir_.relativeFilePath(native_info.absoluteDir().path());
  const QString native_file_contents = native_file.readAll();

  assert(host_platform_icon_.has_value());
  FileData data{.file_name = native_file_name,
                .file_path = native_file_path,
                .proj_relative_dir_path = proj_relative_dir_path,
                .file_contents = native_file_contents,
                .host_platform_display_name = host_platform_display_name_,
                .host_platform_icon = host_platform_icon_.value().get(),
                .platform_file = file};

  auto native_node = new FileView(data, this);
  connect(native_node, &FileView::file_modified, this,
          [this, native_node](const FileData& file_data, const bool modified) {
            const int tab_index = indexOf(native_node);
            setTabText(tab_index, modified ? file_data.modified_display()
                                           : file_data.display());
            Q_EMIT file_modified(modified);
          });
  const QString tab_display = data.display();
  const int tab_index =
      addTab(native_node, AssetCache::iprm_nativefile_icon(), tab_display);
  tabBar()->setTabData(tab_index, native_file_path);
  setCurrentIndex(tab_index);
  setTabToolTip(tab_index, tab_display);
  open_files_[native_file_path] = native_node;
  return native_node;
}

void Project::add_backend(const BackendFile& file_node) {
  auto path = file_node.path.generic_string();
  auto file_path_str = QString::fromStdString(path);
  QFile backend_file(file_path_str);
  if (!backend_file.open(QIODevice::ReadOnly | QIODevice::Text)) {
    return;
  }
  const auto native_file_path = QDir::toNativeSeparators(
      QString::fromStdString(file_node.native_path.string()));
  auto native_node_itr = open_files_.find(native_file_path);
  if (native_node_itr != open_files_.end()) {
    FileView* native_node = native_node_itr.value();
    native_node->show_backend(file_node.backend.get(), backend_file.readAll());
    setCurrentWidget(native_node);
  } else {
    if (FileView* native_node = add_native(native_file_path)) {
      native_node->show_backend(file_node.backend.get(), backend_file.readAll());
      setCurrentWidget(native_node);
    }
  }
}

FileView* Project::current_file() const {
  return qobject_cast<FileView*>(currentWidget());
}

void Project::close_file(FileView* file) {
  const int tab_index = indexOf(file);
  const auto native_file_path = tabBar()->tabData(tab_index).toString();
  removeTab(tab_index);
  file->deleteLater();
  open_files_.remove(native_file_path);
  Q_EMIT file_closed(static_cast<int>(open_files_.size()));
}

void Project::on_file_tab_closed(const int tab_index) {
  const auto native_file_path = tabBar()->tabData(tab_index).toString();
  auto file_node = qobject_cast<FileView*>(widget(tab_index));
  removeTab(tab_index);
  file_node->deleteLater();
  open_files_.remove(native_file_path);
  Q_EMIT file_closed(static_cast<int>(open_files_.size()));
}

void Project::on_file_tab_changed(const int tab_index) {
  if (auto file_node = qobject_cast<const FileView*>(widget(tab_index))) {
    Q_EMIT file_modified(file_node->is_modified());
  }
}

}  // namespace iprm
