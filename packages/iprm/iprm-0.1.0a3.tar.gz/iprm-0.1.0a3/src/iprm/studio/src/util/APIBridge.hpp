/*
 * Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>
 *
 * SPDX-License-Identifier: MIT
 */
#pragma once

#include "../../../core/src/TypeFlags.hpp"
#include "APIError.hpp"
#include "graphviz.hpp"

#include <pybind11/embed.h>
#include <pybind11/pybind11.h>
#include <QDir>
#include <QHash>
#include <QIcon>
#include <QObject>
#include <QString>
#include <QThread>
#include <QVariant>

#include <functional>
#include <optional>
#include <variant>

namespace py = pybind11;

namespace iprm {

struct CurrentSourceDir {};
struct SourceDir {
  QString path;
};
struct RootRelativeSourceDir {
  QString path;
};
struct CurrentBinaryDir {};
struct BinaryDir {
  QString path;
};
struct RootRelativeBinaryDir {
  QString path;
};
using Dir = std::variant<CurrentSourceDir,
                         SourceDir,
                         RootRelativeSourceDir,
                         CurrentBinaryDir,
                         BinaryDir,
                         RootRelativeBinaryDir>;

struct Object {
  QString name;
  QString type_name;
  TypeFlags type;
  QVariantHash properties;
  QString hex_colour;
  QString shape_type;
  QString project_rel_dir_path;
  QIcon icon;

  QStringList dependencies() const {
    return properties["dependencies"].toStringList();
  }
};

struct PlatformFile {
  QList<Object> objects_;
  QIcon icon_;
};

struct PlatformProject {
  QHash<QString, PlatformFile> files_;
};

#if defined(__GNUC__)
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wattributes"
#endif

struct Platform {
  std::optional<py::object> native_loader_;
  QHash<QString, QList<Object>> objs_;
  gv::ctx_ptr_t gvc_{nullptr};
  gv::graph_ptr_t dep_graph_{nullptr};
  std::optional<gv::LayoutResult> dep_graph_layout_;
};

struct BackendGenerate {};
struct BackendConfigure {
  QStringList args_;
};
struct BackendBuild {
  QStringList args_;
};
struct BackendTest {
  QStringList args_;
};
struct BackendInstall {
  QStringList args_;
};

using BackendCommand = std::variant<BackendGenerate,
                                    BackendConfigure,
                                    BackendBuild,
                                    BackendTest,
                                    BackendInstall>;

enum class BackendType { Builtin, Plugin };

struct SystemBackend {
  py::object klass_;
  std::vector<std::string> file_exts_;
  QString name_;
  QIcon icon_;
  BackendType type_{BackendType::Builtin};
  std::vector<BackendCommand> commands_;
};

struct APICategoryEntry {
  TypeFlags type_{TypeFlags::NONE};
  QIcon icon_;
};

class APIBridge : public QObject {
  Q_OBJECT

  friend class APIBridgeThread;

 public:
  explicit APIBridge(const QDir& iprm_src_dir, QObject* parent = nullptr);
  ~APIBridge();

  APIBridge(const APIBridge&) = delete;
  APIBridge& operator=(const APIBridge&) = delete;

  void set_root_dir(const QDir& root_dir);

  void set_external_plugins_dir(const QDir& external_plugins_dir);

  QStringList platforms() const;

  const QList<SystemBackend>& builtin_backends() const {
    return builtin_backends_;
  }

  const QList<SystemBackend>& plugin_backends() const {
    return plugin_backends_;
  }

  const std::optional<QDir>& external_plugins_dir() const {
    return external_plugins_dir_;
  }

  const QIcon& icon(const QString& platform) const;

  const QString& display(const QString& platform) const;

  QString host_platform_display_name() const {
    return host_platform_display_name_;
  }

  const std::vector<std::filesystem::path>& file_paths() const {
    return file_paths_;
  }

  const QString& version() const { return version_; }

  const QString& copyright() const { return copyright_; }

  const std::string& native_file_name() const { return native_file_name_; }

  const gv::LayoutResult& dependency_graph_layout(
      const QString& platform) const;

  const QHash<QString, QList<Object>>& objects(const QString& platform) const;

  static const QHash<QString, QString>& platform_names() {
    return platform_names_;
  }

  static const QStringList& supported_platform_names() {
    return supported_platform_names_;
  }

  // TODO: Don't make these static, get owner of APIBridge instance to pass
  //  them directly to the contexts that need them
  static const QHash<QString, QHash<QString, APICategoryEntry>>& public_api() {
    return public_api_;
  }

  static const QHash<QString, QHash<QString, APICategoryEntry>>&
  public_objects_api() {
    return public_objects_api_;
  }

 public Q_SLOTS:
  void capture_io();
  void load_builtin_backends();
  void load_plugins(const QDir& plugin_dir);
  void init_sess();
  void destroy_sess();
  void load_project();
  void load_project_file(const QString& file_path);

 Q_SIGNALS:
  void error(const APIError& error) const;

  void print_stdout(const QString& message);
  // TODO: print_stderr

  void project_load_success();

  void project_file_load_success(
      const QHash<QString, PlatformFile>& platform_file);
  void project_file_load_failure(const APIError& error);

 private:
  void populate_api(const py::dict& categories,
                    QHash<QString, QHash<QString, APICategoryEntry>>& api);

  void process_objects(Platform& platform, const py::dict& py_objects) const;

  Object make_object(const QString& file_path, const py::handle& py_obj) const;

  QVariantHash make_object_properties(const py::dict& py_obj_properties) const;

  void build_dependency_graph(Platform& platform_ctx) const;

  void generate(const py::object& generator_class,
                const std::function<void()>& notify_success);

  // TODO: Qt-ify all member variables/APIs and remove most use of STL, as that
  //  is only required for interop with pybind11

  QDir root_dir_;
  std::optional<QDir> external_plugins_dir_;
  std::optional<py::object> sess_;
  QString version_;
  QString copyright_;
  std::string native_file_name_;
  std::vector<std::filesystem::path> file_paths_;
  QString host_platform_display_name_;
  // TODO: Change this into a QHash
  std::unordered_map<QString, Platform> platforms_;

  QList<SystemBackend> builtin_backends_;
  QList<SystemBackend> plugin_backends_;
  QHash<QString, QIcon> plugin_object_icons_;

  std::optional<py::module> iprm_util_platform_;
  std::optional<py::module> iprm_util_loader_;
  std::optional<py::object> iprm_util_dir_klass_;

  inline static QHash<QString, QString> platform_names_;
  inline static QStringList supported_platform_names_;

  inline static QHash<QString, QHash<QString, APICategoryEntry>>
      public_objects_api_;
  inline static QHash<QString, QHash<QString, APICategoryEntry>>
      public_utility_api_;
  inline static QHash<QString, QHash<QString, APICategoryEntry>> public_api_;
};

class APIBridgeThread : public QThread {
  Q_OBJECT

 public:
  explicit APIBridgeThread(const QDir& iprm_src_dir);

  void set_root_dir(const QDir& root_dir);

  void set_external_plugins_dir(const QDir& external_plugins_dir);

  const QString& version() const { return bridge_.version(); }

  const QString& copyright() const { return bridge_.copyright(); }

  const std::string& native_file_name() const {
    return bridge_.native_file_name();
  }

  const std::vector<std::filesystem::path>& file_paths() const {
    return bridge_.file_paths();
  }

  QStringList platforms() const { return bridge_.platforms(); }

  const QList<SystemBackend>& builtin_backends() const {
    return bridge_.builtin_backends();
  }

  const QList<SystemBackend>& plugin_backends() const {
    return bridge_.plugin_backends();
  }

  const std::optional<QDir>& external_plugins_dir() const {
    return bridge_.external_plugins_dir();
  }

  const QIcon& icon(const QString& platform) const {
    return bridge_.icon(platform);
  }

  const QString& display(const QString& platform) const {
    return bridge_.display(platform);
  }

  QString host_platform_display_name() const {
    return bridge_.host_platform_display_name();
  }

  const gv::LayoutResult& dependency_graph_layout(
      const QString& platform) const {
    return bridge_.dependency_graph_layout(platform);
  }

  const QHash<QString, QList<Object>>& objects(const QString& platform) const {
    return bridge_.objects(platform);
  }

 public Q_SLOTS:
  void capture_io();
  void load_builtin_backends();
  void load_plugins(const QDir& plugin_dir);
  void destroy_sess();
  void load_project();
  void load_project_file(const QString& file_path);

 Q_SIGNALS:
  void error(const APIError& error);

  void print_stdout(const QString& message);

  void project_load_success();

  void project_file_load_success(
      const QHash<QString, PlatformFile>& platform_file);
  void project_file_load_failure(const APIError& error);

 private:
  QDir root_dir_;
  py::scoped_interpreter interp_;
  APIBridge bridge_;
};

#if defined(__GNUC__)
#pragma GCC diagnostic pop
#endif

}  // namespace iprm

Q_DECLARE_METATYPE(iprm::PlatformFile)
Q_DECLARE_METATYPE(iprm::CurrentSourceDir)
Q_DECLARE_METATYPE(iprm::SourceDir)
Q_DECLARE_METATYPE(iprm::RootRelativeSourceDir)
Q_DECLARE_METATYPE(iprm::CurrentBinaryDir)
Q_DECLARE_METATYPE(iprm::BinaryDir)
Q_DECLARE_METATYPE(iprm::RootRelativeBinaryDir)
