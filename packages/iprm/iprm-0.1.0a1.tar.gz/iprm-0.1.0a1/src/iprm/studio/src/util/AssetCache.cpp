/*
 * Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>
 *
 * SPDX-License-Identifier: MIT
 */
#include "AssetCache.hpp"
#include <QPainter>
#include <QSvgRenderer>

namespace iprm {

const QIcon& AssetCache::iprm_icon() {
  static QIcon s_iprm_icon(make_svg_icon(":/logos/iprm.svg"));
  return s_iprm_icon;
}

const QIcon& AssetCache::iprm_project_icon() {
  static QIcon s_iprm_project_icon(make_svg_icon(":/icons/project.svg"));
  return s_iprm_project_icon;
}

const QIcon& AssetCache::iprm_subdir_icon() {
  static QIcon s_iprm_subdir_icon(make_svg_icon(":/icons/subdir.svg"));
  return s_iprm_subdir_icon;
}

const QIcon& AssetCache::iprm_nativefile_icon() {
  static QIcon s_iprm_nativefile_icon(make_svg_icon(":/icons/nativefile.svg"));
  return s_iprm_nativefile_icon;
}

const QIcon& AssetCache::builder_icon() {
  static QIcon s_builder_icon(make_svg_icon(":/icons/builder.svg"));
  return s_builder_icon;
}

const QIcon& AssetCache::env_icon() {
  static QIcon s_env_icon(make_svg_icon(":/icons/env.svg"));
  return s_env_icon;
}

const QIcon& AssetCache::folder_icon() {
  static QIcon s_folder_icon(make_svg_icon(":/icons/folder.svg"));
  return s_folder_icon;
}

const QIcon& AssetCache::cmake_icon() {
  static QIcon s_cmake_icon(make_svg_icon(":/logos/cmake.svg"));
  return s_cmake_icon;
}

const QIcon& AssetCache::meson_icon() {
  static QIcon s_meson_icon(make_png_icon(":/logos/meson.png"));
  return s_meson_icon;
}

const QIcon& AssetCache::scons_icon() {
  static QIcon s_scons_icon(make_png_icon(":/logos/scons.png"));
  return s_scons_icon;
}

const QIcon& AssetCache::msbuild_icon() {
  static QIcon s_msbuild_icon(make_svg_icon(":/logos/msbuild.svg"));
  return s_msbuild_icon;
}

const QIcon& AssetCache::windows_icon() {
  static QIcon s_windows_icon(make_svg_icon(":/logos/windows.svg"));
  return s_windows_icon;
}

const QIcon& AssetCache::macos_icon() {
  static QIcon s_macos_icon(make_svg_icon(":/logos/macos2.svg"));
  return s_macos_icon;
}
const QIcon& AssetCache::linux_icon() {
  static QIcon s_linux_icon(make_svg_icon(":/logos/linux.svg"));
  return s_linux_icon;
}

const QIcon& AssetCache::wasm_icon() {
  static QIcon s_wasm_icon(make_svg_icon(":/logos/wasm.svg"));
  return s_wasm_icon;
}

const QIcon& AssetCache::platform_icon(const QString& platform_name) {
  const auto platform_icon = platform_icon_lookup_[platform_name];
  assert(platform_icon.has_value());
  return platform_icon.value().get();
}

const QIcon& AssetCache::host_platform_icon() {
  const auto& host_platform_icon = host_platform_icon_;
  assert(host_platform_icon.has_value());
  return host_platform_icon.value().get();
}

const QIcon& AssetCache::cpp_icon() {
  return svg_type_icon(TypeFlags::CPP, ":/logos/cpp.svg");
}

const QIcon& AssetCache::rust_icon() {
  return png_type_icon(TypeFlags::RUST, ":/logos/rust.png");
}

const QIcon& AssetCache::object_type_icon(TypeFlags type) {
  if (static_cast<bool>(type & TypeFlags::THIRDPARTY)) {
    if (static_cast<bool>(type & TypeFlags::QT)) {
      return qt_icon();
    }
  }
  if (static_cast<bool>(type & TypeFlags::CPP)) {
    return cpp_icon();
  } else if (static_cast<bool>(type & TypeFlags::RUST)) {
    return rust_icon();
  } else if (static_cast<bool>(type & TypeFlags::PROJECT)) {
    return iprm_project_icon();
  } else if (static_cast<bool>(type & TypeFlags::SUBDIR)) {
    return iprm_subdir_icon();
  }
  static QIcon no_icon;
  return no_icon;
}

const QIcon& AssetCache::msvc_icon() {
  return svg_type_icon(TypeFlags::MSVC, ":/logos/visualstudio.svg");
}

const QIcon& AssetCache::clang_icon() {
  return png_type_icon(TypeFlags::CLANG, ":/logos/llvm.png");
}

const QIcon& AssetCache::gcc_icon() {
  return svg_type_icon(TypeFlags::GCC, ":/logos/gcc.svg");
}

const QIcon& AssetCache::qt_icon() {
  return svg_type_icon(TypeFlags::QT, ":/logos/qt.svg");
}

const QIcon& AssetCache::archive_icon() {
  return svg_type_icon(TypeFlags::ARCHIVE, ":/icons/archive.svg");
}

const QIcon& AssetCache::git_icon() {
  return svg_type_icon(TypeFlags::GIT, ":/logos/git.svg");
}

const QIcon& AssetCache::homebrew_icon() {
  return svg_type_icon(TypeFlags::HOMEBREW, ":/logos/homebrew.svg");
}

const QIcon& AssetCache::pkgconfig_icon() {
  return svg_type_icon(TypeFlags::PKGCONFIG, ":/logos/freedesktop.svg");
}

const QIcon& AssetCache::dpkg_icon() {
  return svg_type_icon(TypeFlags::DPKG, ":/logos/debian.svg");
}

const QIcon& AssetCache::rpm_icon() {
  return svg_type_icon(TypeFlags::RPM, ":/logos/redhat.svg");
}

const QIcon& AssetCache::svg_type_icon(TypeFlags type,
                                       const QString& image_path) {
  return type_icon(type, image_path, IconFormat::Svg);
}

const QIcon& AssetCache::png_type_icon(TypeFlags type,
                                       const QString& image_path) {
  return type_icon(type, image_path, IconFormat::Png);
}

const QIcon& AssetCache::type_icon(TypeFlags type,
                                   const QString& image_path,
                                   IconFormat format) {
  auto icon_itr = type_icons_.find(type);
  if (icon_itr != type_icons_.end()) {
    return *icon_itr;
  }
  type_icons_[type] = make_icon(image_path, format);
  return type_icons_[type];
}

QIcon AssetCache::make_png_icon(const QString& image_path) {
  QPixmap pixmap(image_path);
  return QIcon(pixmap.scaled(icon_size()));
}

QIcon AssetCache::make_svg_icon(const QString& image_path) {
  QSvgRenderer renderer(image_path);
  QPixmap pixmap(icon_size());
  pixmap.fill(Qt::transparent);
  QPainter painter(&pixmap);
  painter.setRenderHint(QPainter::Antialiasing);
  renderer.render(&painter);
  painter.end();
  QIcon icon;
  icon.addPixmap(pixmap);
  return icon;
}

QIcon AssetCache::make_icon(const QString& image_path, IconFormat format) {
  switch (format) {
    case IconFormat::Svg:
      return make_svg_icon(image_path);
    case IconFormat::Png:
    default:
      return make_png_icon(image_path);
  }
}

const QIcon& AssetCache::colour_icon(const QString& hex_colour) {
  auto icon_itr = colour_icons_.find(hex_colour);
  if (icon_itr != colour_icons_.end()) {
    return *icon_itr;
  }

  const auto size = icon_size();
  QPixmap pixmap(size);
  pixmap.fill(Qt::transparent);
  QPainter painter(&pixmap);
  painter.setRenderHint(QPainter::Antialiasing);
  painter.setPen(Qt::NoPen);
  painter.setBrush(QColor::fromString(hex_colour));
  painter.drawRect(1, 1, size.width() - 2, size.height() - 2);
  painter.end();

  colour_icons_[hex_colour] = QIcon(pixmap);
  return colour_icons_[hex_colour];
}

const QIcon& AssetCache::png_icon(const QString& image_path) {
  auto icon_itr = png_icons_.find(image_path);
  if (icon_itr != png_icons_.end()) {
    return *icon_itr;
  }
  png_icons_[image_path] = make_png_icon(image_path);
  return png_icons_[image_path];
}

const QIcon& AssetCache::svg_icon(const QString& image_path) {
  auto icon_itr = svg_icons_.find(image_path);
  if (icon_itr != svg_icons_.end()) {
    return *icon_itr;
  }
  svg_icons_[image_path] = make_svg_icon(image_path);
  return svg_icons_[image_path];
}

QSize AssetCache::icon_size() {
  return QSize(16, 16);
}

}  // namespace iprm