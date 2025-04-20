/*
 * Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>
 *
 * SPDX-License-Identifier: MIT
 */
#pragma once

#include "../util/APIBridge.hpp"
#include "ObjectsModel.hpp"

#include <QWidget>

class QTabWidget;
class QCodeEditor;

namespace iprm {

class NativeText;
class CMakeText;
class MesonText;
class ObjectsView;
class ObjectPropertiesView;

struct FileData {
  QString file_name;
  QString file_path;
  QString proj_relative_dir_path;
  QString file_contents;
  QString host_platform_display_name;
  const QIcon& host_platform_icon;
  QHash<QString, PlatformFile> platform_file;

  QString display() const {
    return QString("%0 (%1)").arg(file_name, proj_relative_dir_path);
  }

  QString modified_display() const { return QString("* %0").arg(display()); }
};

class FileView : public QWidget {
  Q_OBJECT
 public:
  FileView(const FileData& file_data, QWidget* parent = nullptr);

  void show_backend(const SystemBackend& backend, QString contents);

  const FileData& file_data() const { return saved_file_data_; }

  bool is_modified() const { return is_modified_; }

  const QString& modified_file_contents() const {
    return modified_file_contents_;
  }

  void update_data(const QString& file_contents,
                   const QHash<QString, PlatformFile>& platform_file);

 Q_SIGNALS:
  void file_modified(const FileData& file_data, bool modified);

 private Q_SLOTS:
  void on_object_selected(ObjectNodeEntry& object);

 private:
  FileData saved_file_data_;
  QString modified_file_contents_;
  bool is_modified_{false};
  ObjectsView* objects_view_{nullptr};
  ObjectPropertiesView* object_properties_view_{nullptr};
  QTabWidget* text_view_{nullptr};
  NativeText* native_text_view_{nullptr};

  struct Backend {
    QTabWidget* backend_text_{nullptr};
    QCodeEditor* backend_text_view_{nullptr};
  };
  QHash<QString, Backend> backend_views_;
};

}  // namespace iprm

Q_DECLARE_METATYPE(iprm::FileData)
