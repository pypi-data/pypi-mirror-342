/*
 * Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>
 *
 * SPDX-License-Identifier: MIT
 */
#include "FileView.hpp"
#include "../util/AssetCache.hpp"
#include "../util/AppTheme.hpp"
#include "NativeText.hpp"
#include "CMakeHighligher.hpp"
#include "ObjectPropertiesView.hpp"
#include "ObjectsModel.hpp"
#include "ObjectsView.hpp"
#include "TextStyle.hpp"

#include <QCodeEditor>
#include <QPythonHighlighter>
#include <QXMLHighlighter>

#include <QLabel>
#include <QPainter>
#include <QSplitter>
#include <QStyleHints>
#include <QSvgRenderer>
#include <QTabWidget>
#include <QVBoxLayout>

namespace iprm {

static const QHash<QString, QStyleSyntaxHighlighter* (*)()>
    builtin_code_highlighters{
        {"CMake",
         []() -> QStyleSyntaxHighlighter* { return new CMakeHighlighter; }},
        {"Meson",
         []() -> QStyleSyntaxHighlighter* { return new QPythonHighlighter; }},
        {"SCons",
         []() -> QStyleSyntaxHighlighter* { return new QPythonHighlighter; }},
        {"MSBuild",
         []() -> QStyleSyntaxHighlighter* { return new QXMLHighlighter; }}};



FileView::FileView(const FileData& file_data, QWidget* parent)
    : QWidget(parent), saved_file_data_(file_data) {
  qRegisterMetaType<FileData>();
  auto view = new QSplitter(Qt::Horizontal, this);
  auto gui_view = new QSplitter(Qt::Horizontal, this);
  objects_view_ = new ObjectsView(this);
  connect(objects_view_, &ObjectsView::object_selected, this,
          &FileView::on_object_selected);
  objects_view_->load(saved_file_data_.platform_file);
  gui_view->addWidget(objects_view_);

  object_properties_view_ = new ObjectPropertiesView(this);
  gui_view->addWidget(object_properties_view_);
  gui_view->setSizes({300, 400});

  text_view_ = new QTabWidget(this);
  text_view_->setMovable(true);

  // TODO: Also generalize these to support native/builtin/plugins without
  //  hardcoding support for each one or needing to have custom classes for each
  native_text_view_ = new NativeText(this);
  native_text_view_->setPlainText(saved_file_data_.file_contents);
  connect(native_text_view_, &NativeText::textChanged, this, [this]() {
    modified_file_contents_ = native_text_view_->toPlainText();
    const bool changed_from_last_save =
        modified_file_contents_ != saved_file_data_.file_contents;
    is_modified_ = changed_from_last_save;
    Q_EMIT file_modified(saved_file_data_, is_modified_);
  });
  connect(&AppTheme::instance(), &AppTheme::scheme_changed, this,
          [this, view](AppTheme::Scheme) {
            native_text_view_->setSyntaxStyle(
                AppTheme::instance().active_text_style());
          });
  text_view_->addTab(native_text_view_, AssetCache::iprm_nativefile_icon(),
                     tr("IPRM"));
  text_view_->setCurrentIndex(0);

  view->addWidget(gui_view);
  view->addWidget(text_view_);

  view->setSizes({400, 300});

  auto main_layout = new QVBoxLayout(this);
  main_layout->addWidget(view);
}

void FileView::update_data(const QString& file_contents,
                           const QHash<QString, PlatformFile>& platform_file) {
  saved_file_data_.file_contents = file_contents;
  saved_file_data_.platform_file = platform_file;
  objects_view_->load(saved_file_data_.platform_file);
  Q_EMIT file_modified(saved_file_data_, false);
  // TODO: reload content in object_properties_view_, remove
  //  objects that no longer exist after reload, and refresh objects content
  //  that do exist still
}

void FileView::show_backend(const SystemBackend& backend, QString contents) {
  if (!backend_views_.contains(backend.name_)) {
    auto& view = backend_views_[backend.name_];
    view.backend_text_ = new QTabWidget(this);
    view.backend_text_view_;
    view.backend_text_view_ = new QCodeEditor(this);
    auto highligher_func_itr = builtin_code_highlighters.find(backend.name_);
    if (highligher_func_itr != builtin_code_highlighters.end()) {
      view.backend_text_view_->setHighlighter((*highligher_func_itr)());
    }
    view.backend_text_view_->setReadOnly(true);
    view.backend_text_view_->setSyntaxStyle(TextStyle::active());
    view.backend_text_view_->setWordWrapMode(QTextOption::NoWrap);

    connect(&AppTheme::instance(), &AppTheme::scheme_changed, this,
            [this, view](AppTheme::Scheme) {
              view.backend_text_view_->setSyntaxStyle(
                  AppTheme::instance().active_text_style());
            });

    view.backend_text_->addTab(view.backend_text_view_,
                               saved_file_data_.host_platform_icon,
                               saved_file_data_.host_platform_display_name);
    text_view_->setTabVisible(
        text_view_->addTab(view.backend_text_, backend.icon_, backend.name_),
        false);
  }

  auto& view = backend_views_[backend.name_];
  auto backend_contents = std::move(contents);
  view.backend_text_view_->setText(
      backend_contents.replace(QChar('\t'), QString(" ").repeated(4)));
  const int backend_tab_index = text_view_->indexOf(view.backend_text_);
  text_view_->setTabVisible(backend_tab_index, true);
  text_view_->setCurrentIndex(backend_tab_index);
}

void FileView::on_object_selected(ObjectNodeEntry& object) {
  object_properties_view_->show(object);
}

}  // namespace iprm
