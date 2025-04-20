/*
 * Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>
 *
 * SPDX-License-Identifier: MIT
 */
#include "DependencyGraphNodeSummary.hpp"
#include "../../../core/src/TypeFlags.hpp"
#include "../util/AssetCache.hpp"
#include "DependencyGraphNode.hpp"
#include "DependencyGraphicsView.hpp"

#include <QLabel>
#include <QStackedWidget>
#include <QVBoxLayout>

namespace iprm {

DependencyGraphNodeSummary::DependencyGraphNodeSummary(
    DependencyGraphicsView& graphics_view)
    : QGraphicsProxyWidget(nullptr), graphics_view_(graphics_view) {
  summary_view_ = new QStackedWidget();
  summary_view_->hide();
  setWidget(summary_view_);
  setZValue(std::numeric_limits<qreal>::max());
  setFlag(ItemIgnoresTransformations, true);

  connect(&graphics_view_, &DependencyGraphicsView::viewport_changed, this,
          &DependencyGraphNodeSummary::update_position);
  connect(this, &DependencyGraphNodeSummary::geometryChanged, this,
          &DependencyGraphNodeSummary::update_position);
}

void DependencyGraphNodeSummary::on_hover_state_changed(
    DependencyGraphNode* node,
    bool hovering) {
  if (!hovering) {
    widget()->hide();
    return;
  }

  auto summary_itr = summaries_.find(node->id());
  if (summary_itr != summaries_.end()) {
    summary_view_->setCurrentWidget(summary_itr->second);
  } else {
    auto summary = new QFrame();
    summary->setFrameShape(QFrame::Box);
    summary->setFrameShadow(QFrame::Plain);
    summary->setLineWidth(2);
    auto main_layout = new QVBoxLayout(summary);
    main_layout->setAlignment(Qt::AlignCenter);

    auto name_label = new QLabel(node->name());
    QFont name_font = name_label->font();
    name_font.setBold(true);
    name_font.setPointSize(12);
    name_label->setFont(name_font);
    main_layout->addWidget(name_label, 0, Qt::AlignHCenter);

    auto name_divider = new QFrame();
    name_divider->setFrameShape(QFrame::HLine);
    name_divider->setFrameShadow(QFrame::Plain);
    name_divider->setLineWidth(1);
    main_layout->addWidget(name_divider);

    auto type_icon_layout = new QHBoxLayout();
    const auto type_flags = node->type_flags();
    const auto icon_size = AssetCache::icon_size();
    auto make_icon_label = [&summary, &type_flags, &icon_size](
                               TypeFlags type, const QIcon& icon) {
      QLabel* label = nullptr;
      if (static_cast<bool>(type_flags & type)) {
        label = new QLabel(summary);
        label->setPixmap(icon.pixmap(icon_size));
      }
      return label;
    };

    type_icon_layout->addStretch(1);

    // Language
    if (auto cpp_label =
            make_icon_label(TypeFlags::CPP, AssetCache::cpp_icon())) {
      type_icon_layout->addWidget(cpp_label);
    } else if (auto rust_label =
                   make_icon_label(TypeFlags::RUST, AssetCache::rust_icon())) {
      type_icon_layout->addWidget(rust_label);
    }

    // Compiler
    if (auto msvc_label =
            make_icon_label(TypeFlags::MSVC, AssetCache::msvc_icon())) {
      type_icon_layout->addWidget(msvc_label);
    } else if (auto clang_label = make_icon_label(TypeFlags::CLANG,
                                                  AssetCache::clang_icon())) {
      type_icon_layout->addWidget(clang_label);
    } else if (auto gcc_label =
                   make_icon_label(TypeFlags::GCC, AssetCache::gcc_icon())) {
      type_icon_layout->addWidget(gcc_label);
    }
    // NOTE: Since Rust only has a single production-ready compiler, we bundle
    //  the compiler and the language logo together

    // Known Third Party
    // TODO: Remove all builtint third party
    if (auto qt_label =
                   make_icon_label(TypeFlags::QT, AssetCache::qt_icon())) {
      type_icon_layout->addWidget(qt_label);
    }

    const QIcon& node_icon = node->icon();
    if (!node_icon.isNull()) {
      auto label = new QLabel(summary);
      label->setPixmap(node_icon.pixmap(icon_size));
      type_icon_layout->addWidget(label);
    }

    // Third Party Content Source
    if (auto archive_label =
            make_icon_label(TypeFlags::ARCHIVE, AssetCache::archive_icon())) {
      type_icon_layout->addWidget(archive_label);
    } else if (auto git_label =
                   make_icon_label(TypeFlags::GIT, AssetCache::git_icon())) {
      type_icon_layout->addWidget(git_label);
    } else if (auto homebrew_label = make_icon_label(
                   TypeFlags::HOMEBREW, AssetCache::homebrew_icon())) {
      type_icon_layout->addWidget(homebrew_label);
    } else if (auto pkgconfig_label = make_icon_label(
                   TypeFlags::PKGCONFIG, AssetCache::pkgconfig_icon())) {
      type_icon_layout->addWidget(pkgconfig_label);
    } else if (auto dpkg_label =
                   make_icon_label(TypeFlags::DPKG, AssetCache::dpkg_icon())) {
      type_icon_layout->addWidget(dpkg_label);
    } else if (auto rpm_label =
                   make_icon_label(TypeFlags::RPM, AssetCache::rpm_icon())) {
      type_icon_layout->addWidget(rpm_label);
    }
    // TODO: Add remaining third party source content icons when they are
    //  supported

    type_icon_layout->addStretch(1);

    main_layout->addLayout(type_icon_layout);
    main_layout->addWidget(new QLabel(node->target_type()), 0,
                           Qt::AlignHCenter);

    auto type_divider = new QFrame();
    type_divider->setFrameShape(QFrame::HLine);
    type_divider->setFrameShadow(QFrame::Plain);
    type_divider->setLineWidth(1);
    main_layout->addWidget(type_divider);

    main_layout->addWidget(new QLabel(node->obj_project_rel_dir_path()), 0,
                           Qt::AlignHCenter);

    summary_view_->addWidget(summary);
    summary_view_->setCurrentWidget(summary);
    summaries_[node->id()] = summary;
  }
  widget()->setVisible(hovering);
}

void DependencyGraphNodeSummary::update_position() {
  setPos(graphics_view_.mapToScene(QPoint(
      10, graphics_view_.viewport()->height() - 10 - widget()->height())));
}

}  // namespace iprm
