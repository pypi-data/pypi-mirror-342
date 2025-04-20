/*
 * Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>
 *
 * SPDX-License-Identifier: MIT
 */
#include "APIBridge.hpp"
#include "AssetCache.hpp"

#include <pybind11/embed.h>
#include <QList>
#include <QString>

#include <ranges>

namespace iprm {

APIError make_error(const QString& err_msg,
                    const pybind11::error_already_set& e) {
  const char* py_err_details = e.what();
  const QString err_details =
      QByteArray::fromRawData(py_err_details, std::strlen(py_err_details));
  return APIError(QString("%0: %1").arg(err_msg, err_details));
}

APIBridge::APIBridge(QObject* parent) : QObject(parent) {
  qRegisterMetaType<APIError>();
  qRegisterMetaType<PlatformFile>();
}


APIBridge::~APIBridge() {
  if (iprm_util_platform_.has_value()) {
    iprm_util_platform_.value().release();
    iprm_util_platform_.reset();
  }
  if (iprm_util_loader_.has_value()) {
    iprm_util_loader_.value().release();
    iprm_util_loader_.reset();
  }
}

void APIBridge::set_root_dir(const QDir& root_dir) {
  root_dir_ = root_dir;
}

void APIBridge::set_external_plugins_dir(const QDir& external_plugins_dir) {
  external_plugins_dir_ = external_plugins_dir;
}

QStringList APIBridge::platforms() const {
  QStringList platforms;
  platforms.reserve(platforms_.size());
  for (const auto& platform : platforms_) {
    platforms.push_back(platform.first);
  }
  return platforms;
}

const QIcon& APIBridge::icon(const QString& platform) const {
  static const QIcon s_no_platform;
  const auto platform_icon_itr =
      AssetCache::platform_icon_lookup_.find(platform);
  if (platform_icon_itr == AssetCache::platform_icon_lookup_.end()) {
    return s_no_platform;
  }
  const auto& platform_icon = platform_icon_itr->second;
  assert(platform_icon.has_value());
  return platform_icon.value().get();
}

const QString& APIBridge::display(const QString& platform) const {
  static const QString s_no_platform;
  const auto platform_display_itr = platform_names_.find(platform);
  if (platform_display_itr == platform_names_.end()) {
    return s_no_platform;
  }

  return platform_display_itr.value();
}

const QHash<QString, QList<ObjectNode>>& APIBridge::objects(
    const QString& platform) const {
  static const QHash<QString, QList<ObjectNode>> s_no_platform;

  const auto platform_itr = platforms_.find(platform);
  if (platform_itr == platforms_.end()) {
    return s_no_platform;
  }
  return platform_itr->second.objs_;
}

const gv::LayoutResult& APIBridge::dependency_graph_layout(
    const QString& platform) const {
  static gv::LayoutResult s_no_dep_graph;

  const auto platform_itr = platforms_.find(platform);
  if (platform_itr == platforms_.end()) {
    return s_no_dep_graph;
  } else if (platform_itr->second.dep_graph_layout_.has_value()) {
    return platform_itr->second.dep_graph_layout_.value();
  }
  return s_no_dep_graph;
}

void APIBridge::capture_io() {
  try {
    py::module builtins = py::module::import("builtins");
    py::cpp_function print([this](py::args args, py::kwargs kwargs) {
      // TODO: Handle stderr so we log it as an error
      if (args.size() == 1) {
        Q_EMIT print_stdout(
            QString::fromStdString(args[0].cast<std::string>()));
      }
    });
    builtins.attr("print") = print;
  } catch (const py::error_already_set& e) {
    Q_EMIT error(make_error("Failed to load capture IO", e));
  }
}

std::vector<std::string> get_file_extensions(const py::list& py_file_exts) {
  std::vector<std::string> file_exts;
  file_exts.reserve(py_file_exts.size());
  for (const auto& file_ext : py_file_exts) {
    file_exts.push_back(file_ext.cast<std::string>());
  }
  return file_exts;
}

void APIBridge::load_builtin_backends() {
  struct BuiltinConfig {
    std::string module_name;
    std::string class_name;
    QString bin_dir;
    QIcon icon;
    std::vector<BackendCommand> commands;
  };

  try {
    const QString src_dir = root_dir_.absolutePath();

    // TODO: Query the commands the builtin backend supports and don't hardcode
    //  these arguments, get them from settings if the project and the backend
    //  has them saved, otherwise use these as defaults
    std::vector<BuiltinConfig> backends = {
        {"iprm.backend.cmake",
         "CMake",
         root_dir_.absoluteFilePath("build/cmake"),
         AssetCache::cmake_icon(),
         {BackendGenerate{},
          BackendConfigure{QStringList{}
                           << "--ninja" << "--srcdir" << src_dir << "--bindir"
                           << root_dir_.absoluteFilePath("build/cmake")
                           << "--release"},
          BackendBuild{QStringList{}
                       << "--bindir"
                       << root_dir_.absoluteFilePath("build/cmake")
                       << "--release"},
          BackendTest{QStringList{} << "--bindir"
                                    << root_dir_.absoluteFilePath("build/cmake")
                                    << "--release"}}},
        {"iprm.backend.meson",
         "Meson",
         root_dir_.absoluteFilePath("build/meson"),
         QIcon(":/logos/meson.png"),
         {BackendGenerate{},
          BackendConfigure{QStringList{}
                           << "--ninja" << "--srcdir" << src_dir << "--bindir"
                           << root_dir_.absoluteFilePath("build/meson")
                           << "--release"},
          BackendBuild{QStringList{}
                       << "--bindir"
                       << root_dir_.absoluteFilePath("build/meson")
                       << "--release"},
          BackendTest{QStringList{} << "--bindir"
                                    << root_dir_.absoluteFilePath("build/meson")
                                    << "--release"}}},
        {"iprm.backend.scons",
         "SCons",
         root_dir_.absoluteFilePath("build/scons"),
         QIcon(":/logos/scons.png"),
         {BackendGenerate{},
          BackendBuild{QStringList{}
                       << "--bindir"
                       << root_dir_.absoluteFilePath("build/scons")
                       << "--release"}}}};

#ifdef Q_OS_WIN
    backends.push_back(
        {"iprm.backend.msbuild",
         "MSBuild",
         root_dir_.absoluteFilePath("build/msbuild"),
         AssetCache::msbuild_icon(),
         {BackendGenerate{},
          BackendBuild{QStringList{} << "--bindir" << "build/msbuild"
                                     << "--release" << "--solution"
                                     << "iprm_cli_test"}}});
#endif

    for (const auto& config : backends) {
      auto backend_module = py::module::import(config.module_name.c_str())
                                .attr(config.class_name.c_str());
      const auto file_exts =
          get_file_extensions(backend_module.attr("generate_file_exts")());

      SystemBackend backend{.klass_ = backend_module,
                            .file_exts_ = file_exts,
                            .name_ = QString::fromStdString(config.class_name),
                            .icon_ = config.icon,
                            .type_ = BackendType::Builtin,
                            .commands_ = config.commands};
      builtin_backends_.append(backend);
    }
  } catch (const py::error_already_set& e) {
    Q_EMIT error(make_error("Failed to load builtin backends", e));
  }
}

void APIBridge::load_plugins(const QDir& plugin_dir) {
  try {
    static constexpr char s_svg_icon_path_attr[] = "svg_icon_path";
    static constexpr char s_png_icon_path_attr[] = "png_icon_path";

    auto plugin_icon = [](const py::object& klass) {
      auto icon_path_str = [](const py::object& icon_path) {
        return QString::fromStdString(
            icon_path.attr("__str__")().cast<std::string>());
      };
      if (py::hasattr(klass, s_svg_icon_path_attr)) {
        py::object svg_icon_path = klass.attr("svg_icon_path")();
        if (!svg_icon_path.is_none()) {
          return AssetCache::svg_icon(icon_path_str(svg_icon_path));
        }
      }

      if (py::hasattr(klass, s_png_icon_path_attr)) {
        py::object png_icon_path = klass.attr("png_icon_path")();
        if (!png_icon_path.is_none()) {
          return AssetCache::png_icon(icon_path_str(png_icon_path));
        }
      }
      return QIcon();
    };

    auto iprm_util_plugins = py::module::import("iprm.util.plugins");
    const std::string dir = plugin_dir.absolutePath().toStdString();

    py::dict loaded_backend_plugins =
        iprm_util_plugins.attr("load_backends")(dir);
    for (const auto& [plugin_name, plugin_klass] : loaded_backend_plugins) {
      const auto name = QString::fromStdString(plugin_name.cast<std::string>());
      py::object klass = plugin_klass.cast<py::object>();

      // TODO: Query the commands the plugin backend supports and add the
      //  supported commands
      plugin_backends_.append(SystemBackend{
          .klass_ = klass,
          .file_exts_ = get_file_extensions(klass.attr("generate_file_exts")()),
          .name_ = name,
          .icon_ = plugin_icon(klass),
          .type_ = BackendType::Plugin,
          .commands_ = {BackendGenerate{}}});
    }

    py::dict loaded_object_plugins =
        iprm_util_plugins.attr("load_objects")(dir);
    for (const auto& [plugin_name, plugin_klass] : loaded_object_plugins) {
      const auto name = QString::fromStdString(plugin_name.cast<std::string>());
      py::object klass = plugin_klass.cast<py::object>();
      plugin_object_icons_[name] = plugin_icon(klass);
    }
  } catch (const py::error_already_set& e) {
    Q_EMIT error(make_error("Failed to load plugin backends", e));
  }
}

void APIBridge::init_sess() {
  destroy_sess();
  try {
    auto iprm = py::module::import("iprm");
    version_ =
        QString::fromStdString(iprm.attr("__version__").cast<std::string>());
    copyright_ =
        QString::fromStdString(iprm.attr("__copyright__").cast<std::string>());
    native_file_name_ = iprm.attr("FILE_NAME").cast<std::string>();

    auto iprm_core_session = py::module::import("iprm.core.session");
    if (!iprm_core_session) {
      Q_EMIT error(APIError("Failed to import iprm.core.session module"));
      return;
    }

    const std::string dir = root_dir_.absolutePath().toStdString();
    // Create kwargs dict with default values matching CLI
    // py::dict kwargs;
    // kwargs["use_cache"] = true;  // Match CLI default behavior

    try {
      auto session_class = iprm_core_session.attr("Session");
      session_class.attr("create")(dir);

      py::list loadable_file_paths =
          session_class.attr("retrieve_loadable_files")();

      for (const auto& file_path : loadable_file_paths) {
        file_paths_.emplace_back(file_path.cast<std::string>());
      }

      sess_ = session_class;
    } catch (const py::error_already_set& e) {
      Q_EMIT error(make_error("Failed to create Session", e));
    }

    iprm_util_platform_ = py::module::import("iprm.util.platform");
    iprm_util_loader_ = py::module::import("iprm.util.loader");
  } catch (const py::error_already_set& e) {
    Q_EMIT error(make_error("Error during initialization", e));
  }
}

void APIBridge::destroy_sess() {
  if (!sess_.has_value()) {
    return;
  }
  for (auto& platform : platforms_ | std::views::values) {
    if (platform.native_loader_.has_value()) {
      platform.native_loader_.value().release();
    }
  }
  (void)sess_.value().attr("destroy")();
  sess_.value().release();
  sess_.reset();
}

void APIBridge::load_project() {
  init_sess();
  if (!sess_.has_value() || !iprm_util_platform_.has_value() ||
      !iprm_util_loader_.has_value()) {
    Q_EMIT error(APIError("APIBridge not initialized"));
    return;
  }

  auto& iprm_util_platform = iprm_util_platform_.value();
  auto& iprm_util_loader = iprm_util_loader_.value();

  const py::dict platform_display_lookup =
      iprm_util_platform.attr("PLAT_DISPLAY_NAME");
  for (const auto& [key, value] : platform_display_lookup) {
    const auto name = key.cast<std::string>();
    const auto display_name = value.cast<std::string>();
    platform_names_[QString::fromStdString(name)] =
        QString::fromStdString(display_name);
  }


  const auto iprm_namespace = py::module::import("iprm.api.namespace");
  if (!iprm_namespace) {
    Q_EMIT error(APIError("Failed to import iprm.api.namespace module"));
    return;
  }

  const py::dict public_utility_api =
      iprm_namespace.attr("UTILITY_CATEGORY");
  populate_api(public_utility_api, public_utility_api_);
  public_api_.insert(public_utility_api_);

  const py::dict public_objects_api =
      iprm_namespace.attr("OBJECT_CATEGORIES");
  populate_api(public_objects_api, public_objects_api_);

  QHash<QString, APICategoryEntry> plugin_cpp_objects;

  const auto cpp_category = QString::fromStdString(
      iprm_namespace.attr("CPP_CATAGEORY_KEY").cast<std::string>());

  for (const py::list supported_platforms =
           iprm_util_platform.attr("PLATFORMS");
       const auto& supported_platform : supported_platforms) {
    const auto plat = supported_platform.cast<std::string>();
    const auto platform_name = QString::fromStdString(plat);
    Platform& platform = platforms_[platform_name];

    const std::string dir = root_dir_.absolutePath().toStdString();
    const std::string plugin_dir =
        external_plugins_dir_.has_value()
            ? external_plugins_dir_.value().absolutePath().toStdString()
            : "";
    platform.native_loader_ = iprm_util_loader.attr("Loader")(dir, plat, plugin_dir);
    if (!platform.native_loader_) {
      Q_EMIT error(APIError("Failed to create Loader instance"));
      return;
    }

    try {
      platform.objs_.clear();
      py::handle py_objects =
          platform.native_loader_.value().attr("load_project")();
      if (!py_objects.is_none()) {
        process_objects(platform, py_objects.cast<py::dict>());
        const py::dict plugin_cpp_obj_categories =
            platform.native_loader_.value().attr(
                "plugin_cpp_object_categories");
        for (const auto& [key, value] : plugin_cpp_obj_categories) {
          const auto cpp_obj_name =
              QString::fromStdString(key.cast<std::string>());
          const auto cpp_type_flags =
              static_cast<TypeFlags>(value.cast<std::int64_t>());
          const auto obj_icon_itr = plugin_object_icons_.find(cpp_obj_name);
          plugin_cpp_objects[cpp_obj_name] = APICategoryEntry{
              cpp_type_flags, obj_icon_itr == plugin_object_icons_.end()
                                  ? QIcon{}
                                  : obj_icon_itr.value()};
        }
      } else {
        platforms_.erase(platform_name);
      }

    } catch (const py::error_already_set& e) {
      Q_EMIT error(make_error(QString("Error loading project for platform '%0'")
                                  .arg(platform_names_[platform_name]),
                              e));
    }
  }

  public_objects_api_[cpp_category].insert(plugin_cpp_objects);
  public_api_.insert(public_objects_api_);

  supported_platform_names_.clear();
  for (const auto& platform : platforms_ | std::views::keys) {
    supported_platform_names_.append(platform);
  }

  const auto windows_plat_name = display(QString::fromStdString(
      iprm_util_platform.attr("WINDOWS_PLAT_NAME").cast<std::string>()));
  AssetCache::platform_icon_lookup_[windows_plat_name] =
      AssetCache::windows_icon();

  const auto macos_plat_name = QString::fromStdString(
      iprm_util_platform.attr("MACOS_PLAT_NAME").cast<std::string>());
  const auto macos_plat_display_name = display(macos_plat_name);
  AssetCache::platform_icon_lookup_[macos_plat_name] = AssetCache::macos_icon();
  AssetCache::platform_icon_lookup_[macos_plat_display_name] =
      AssetCache::macos_icon();

  const auto linux_plat_name = display(QString::fromStdString(
      iprm_util_platform.attr("LINUX_PLAT_NAME").cast<std::string>()));
  AssetCache::platform_icon_lookup_[linux_plat_name] = AssetCache::linux_icon();

  const auto wasm_plat_name = display(QString::fromStdString(
      iprm_util_platform.attr("WASM_PLAT_NAME").cast<std::string>()));
  AssetCache::platform_icon_lookup_[wasm_plat_name] = AssetCache::wasm_icon();

  const auto platform = py::module::import("platform");
  if (!platform) {
    Q_EMIT error(APIError("Failed to import platform module"));
    return;
  }
  const auto platform_system =
      QString::fromStdString(platform.attr("system")().cast<std::string>());
  const auto platform_display_itr = platform_names_.find(platform_system);
  const auto platform_icon_itr =
      AssetCache::platform_icon_lookup_.find(platform_system);
  if (platform_display_itr == platform_names_.end() ||
      platform_icon_itr == AssetCache::platform_icon_lookup_.end()) {
    Q_EMIT error(APIError(
        QString("Platform '%0' is not supported").arg(platform_system)));
    return;
  }
  host_platform_display_name_ = platform_display_itr.value();
  AssetCache::host_platform_icon_ = platform_icon_itr->second;

  Q_EMIT project_load_success();
}

void APIBridge::populate_api(
    const py::dict& categories,
    QHash<QString, QHash<QString, APICategoryEntry>>& api) {
  for (const auto& [key, value] : categories) {
    const auto category = QString::fromStdString(key.cast<std::string>());
    const py::list py_types = value.cast<py::list>();
    QHash<QString, APICategoryEntry> entries;
    for (const auto& py_type : py_types) {
      const auto py_type_dict = py_type.cast<py::dict>();
      for (const auto& [py_type_name, py_type_flags] : py_type_dict) {
        const auto type_name =
            QString::fromStdString(py_type_name.cast<std::string>());
        const auto type_flags =
            static_cast<TypeFlags>(py_type_flags.cast<std::int64_t>());

        const QIcon type_icon = [&]() {
          if (category == "Utilities") {
            if (type_name.endsWith("Builder")) {
              return AssetCache::builder_icon();
            } else if (type_name == "Env") {
              return AssetCache::env_icon();
            } else if (type_name.endsWith("Dir")) {
              return AssetCache::folder_icon();
            }
          }
          return AssetCache::object_type_icon(type_flags);
        }();

        entries[type_name] = APICategoryEntry{type_flags, type_icon};
      }
      api.insert(category, entries);
    }
  }
}

void APIBridge::process_objects(Platform& platform,
                                const py::dict& py_objects) const {
  // TODO: setup data for gui/main thread more efficiently here
  for (const auto& [key, value] : py_objects) {
    const auto file_path = key.cast<std::string>();
    const auto normalized_file_path =
        QDir::toNativeSeparators(QString::fromStdString(file_path));
    py::list obj_list = value.cast<py::list>();
    QList<ObjectNode> objects;
    for (const auto& obj : obj_list) {
      objects.push_back(make_object_node(normalized_file_path, obj));
    }
    platform.objs_[normalized_file_path] = std::move(objects);
  }
  build_dependency_graph(platform);
}

ObjectNode APIBridge::make_object_node(const QString& file_path,
                                       const py::handle& py_obj) const {
  const auto obj_name = py_obj.attr("name").cast<std::string>();
  const auto obj_type_name =
      py_obj.get_type().attr("__name__").cast<std::string>();
  const auto obj_type_flags =
      static_cast<TypeFlags>(py_obj.attr("type_flags").cast<std::int64_t>());
  const py::list py_obj_dependencies = py_obj.attr("dependencies");
  std::vector<std::string> obj_dependencies;
  obj_dependencies.reserve(py_obj_dependencies.size());
  for (const auto& obj_dep : py_obj_dependencies) {
    obj_dependencies.push_back(py::cast<std::string>(obj_dep));
  }
  const auto obj_hex_colour = py_obj.attr("hex_colour").cast<std::string>();
  const auto obj_shape_type = py_obj.attr("shape_type").cast<std::string>();
  const auto obj_file_path = QDir::toNativeSeparators(file_path);
  const auto obj_file_dir_path = QFileInfo(obj_file_path).absolutePath();
  const QString proj_relative_dir_path =
      root_dir_.relativeFilePath(obj_file_dir_path);

  ObjectNode obj{
      obj_name,       obj_type_name,  obj_type_flags,        obj_dependencies,
      obj_hex_colour, obj_shape_type, proj_relative_dir_path};
  const auto obj_icon_itr =
      plugin_object_icons_.find(QString::fromStdString(obj_type_name));
  // TODO: Pass the icon to the DependencyGraphNode or remove this and expose
  //  the ability to look it up in DependencyGraphItemFactory
  if (obj_icon_itr != plugin_object_icons_.end()) {
    obj.set_icon(obj_icon_itr.value());
  }
  return obj;
}

void APIBridge::build_dependency_graph(Platform& platform_ctx) const {
  platform_ctx.gvc_.reset(gvContext());
  if (platform_ctx.gvc_ == nullptr) {
    Q_EMIT error(APIError("Dependency graph initialization failed"));
    return;
  }
  platform_ctx.dep_graph_ = gv::create_graph("dependency_graph");

  QHash<QString, Agnode_t*> gv_nodes;
  QHash<QString, TypeFlags> gv_node_types;
  QHash<QString, QIcon> gv_node_icons;

  for (const auto& objects : platform_ctx.objs_) {
    for (const auto& obj : objects) {
      if (static_cast<bool>(obj.type & TypeFlags::TARGET)) {
        gv_node_types[obj.name] = obj.type;
        if (obj.icon.has_value()) {
          gv_node_icons[obj.name] = obj.icon.value();
        }

        const auto node_id = static_cast<int>(gv_nodes.size());

        gv_nodes[obj.name] =
            add_node(platform_ctx.dep_graph_, node_id, obj.name.toStdString(),
                     obj.type_name.toStdString(), obj.shape_type.toStdString(),
                     obj.hex_colour.toStdString(),
                     obj.project_rel_dir_path.toStdString());
      }
    }
  }

  // Second pass: add dependencies
  for (const auto& objects : platform_ctx.objs_) {
    for (const auto& obj : objects) {
      const auto is_target = static_cast<bool>(obj.type & TypeFlags::TARGET);
      if (auto deps = obj.dependencies; is_target) {
        auto source_node = gv_nodes[obj.name];
        for (const auto& dep : deps) {
          auto target_node = gv_nodes[dep];
          add_edge(platform_ctx.dep_graph_, source_node, target_node);
        }
      }
    }
  }

  if (auto layout_res =
          apply_layout(platform_ctx.gvc_, platform_ctx.dep_graph_, "dot")) {
    for (auto& node : layout_res.value().nodes) {
      const auto node_name = QString::fromStdString(node.name);
      const auto node_icon_itr = gv_node_icons.find(node_name);
      if (node_icon_itr != gv_node_icons.end()) {
        node.icon = node_icon_itr.value();
      }
      node.type = gv_node_types[QString::fromStdString(node.name)];
    }
    platform_ctx.dep_graph_layout_ = layout_res.value();
  } else {
    Q_EMIT error(APIError("Dependency graph layout failed"));
  }
}

void APIBridge::load_project_file(const QString& file_path) {
  const auto normalized_file_path = QDir::toNativeSeparators(file_path);
  QHash<QString, PlatformFile> platform_file;
  for (auto& [platform_name, platform_ctx] : platforms_) {
    auto& objects = platform_ctx.objs_[normalized_file_path];
    objects.clear();
    try {
      py::list py_objects = platform_ctx.native_loader_.value().attr(
          "load_project_file")(file_path.toStdString());
      for (const auto& py_obj : py_objects) {
        objects.push_back(make_object_node(file_path, py_obj));
      }
      platform_file.insert(
          platform_name,
          PlatformFile{.objects_ = objects, .icon_ = icon(platform_name)});
    } catch (const py::error_already_set& e) {
      Q_EMIT project_file_load_failure(make_error(
          QString("Error loading project file '%0'").arg(file_path), e));
    }
    build_dependency_graph(platform_ctx);
  }
  Q_EMIT project_file_load_success(platform_file);
}

APIBridgeThread::APIBridgeThread() : QThread(nullptr), bridge_(), interp_() {
  bridge_.moveToThread(this);
  connect(&bridge_, &APIBridge::error, this, &APIBridgeThread::error);
  connect(&bridge_, &APIBridge::print_stdout, this,
          &APIBridgeThread::print_stdout);
  connect(&bridge_, &APIBridge::project_load_success, this,
          &APIBridgeThread::project_load_success);
  connect(&bridge_, &APIBridge::project_file_load_success, this,
          &APIBridgeThread::project_file_load_success);
  connect(&bridge_, &APIBridge::project_file_load_failure, this,
          &APIBridgeThread::project_file_load_failure);
}

void APIBridgeThread::set_root_dir(const QDir& root_dir) {
  bridge_.set_root_dir(root_dir);
}

void APIBridgeThread::set_external_plugins_dir(
    const QDir& external_plugins_dir) {
  bridge_.set_external_plugins_dir(external_plugins_dir);
}

void APIBridgeThread::capture_io() {
  py::gil_scoped_acquire acq;
  bridge_.capture_io();
}

void APIBridgeThread::destroy_sess() {
  py::gil_scoped_acquire acq;
  bridge_.destroy_sess();
}

void APIBridgeThread::load_builtin_backends() {
  py::gil_scoped_acquire acq;
  bridge_.load_builtin_backends();
}

void APIBridgeThread::load_plugins(const QDir& plugin_dir) {
  py::gil_scoped_acquire acq;
  bridge_.load_plugins(plugin_dir);
}

void APIBridgeThread::load_project() {
  py::gil_scoped_acquire acq;
  bridge_.load_project();
}

void APIBridgeThread::load_project_file(const QString& file_path) {
  py::gil_scoped_acquire acq;
  bridge_.load_project_file(file_path);
}


}  // namespace iprm