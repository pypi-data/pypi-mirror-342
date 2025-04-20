/*
 * Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>
 *
 * SPDX-License-Identifier: MIT
 */
#pragma once

#include "../../../core/src/TypeFlags.hpp"

#include <QHash>
#include <QIcon>
#include <QString>

#include <functional>
#include <optional>
#include <unordered_map>

namespace iprm {

class AssetCache {
 public:
  enum class IconFormat {
    Svg,
    Png,
  };

  static QSize icon_size();

  static const QIcon& iprm_icon();
  static const QIcon& iprm_project_icon();
  static const QIcon& iprm_subdir_icon();
  static const QIcon& iprm_nativefile_icon();

  static const QIcon& builder_icon();
  static const QIcon& env_icon();
  static const QIcon& folder_icon();

  static const QIcon& cmake_icon();
  static const QIcon& meson_icon();
  static const QIcon& scons_icon();
  static const QIcon& msbuild_icon();


  static const QIcon& windows_icon();
  static const QIcon& macos_icon();
  static const QIcon& linux_icon();
  static const QIcon& wasm_icon();

  static const QIcon& platform_icon(const QString& platform_name);
  static const QIcon& host_platform_icon();

  // TODO: Create and add the utilities and general object icons from the public
  //  API. Just get royalty free SVG icons online for this purpose

  static const QIcon& cpp_icon();
  static const QIcon& rust_icon();

  // TODO: Add more Target icons (e.g. CustomTarget, ScriptTarget,
  //  PythonScriptTarget, etc)

  static const QIcon& object_type_icon(TypeFlags type);

  static const QIcon& msvc_icon();
  static const QIcon& clang_icon();
  static const QIcon& gcc_icon();

  // TODO: Remove the hardcoded third party libraries and move them to plugins
  static const QIcon& qt_icon();

  static const QIcon& archive_icon();
  static const QIcon& git_icon();
  static const QIcon& homebrew_icon();
  static const QIcon& pkgconfig_icon();
  static const QIcon& dpkg_icon();
  static const QIcon& rpm_icon();
  // TODO: Add the remaining third party content source icons

  static const QIcon& colour_icon(const QString& hex_colour);
  static const QIcon& png_icon(const QString& image_path);
  static const QIcon& svg_icon(const QString& image_path);

  inline static std::optional<std::reference_wrapper<const QIcon>>
      host_platform_icon_;
  inline static std::
      unordered_map<QString, std::optional<std::reference_wrapper<const QIcon>>>
          platform_icon_lookup_;

 private:
  static const QIcon& svg_type_icon(TypeFlags type, const QString& image_path);
  static const QIcon& png_type_icon(TypeFlags type, const QString& image_path);

  static const QIcon& type_icon(TypeFlags type,
                                const QString& image_path,
                                IconFormat format);

  static QIcon make_png_icon(const QString& image_path);
  static QIcon make_svg_icon(const QString& image_path);
  static QIcon make_icon(const QString& image_path, IconFormat format);

  inline static QHash<TypeFlags, QIcon> type_icons_;
  inline static QHash<QString, QIcon> colour_icons_;
  inline static QHash<QString, QIcon> png_icons_;
  inline static QHash<QString, QIcon> svg_icons_;
};

}  // namespace iprm
