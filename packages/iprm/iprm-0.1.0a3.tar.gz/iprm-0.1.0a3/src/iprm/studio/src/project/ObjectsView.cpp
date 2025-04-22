/*
 * Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>
 *
 * SPDX-License-Identifier: MIT
 */
#include "ObjectsView.hpp"
#include "../util/AssetCache.hpp"
#include "ObjectView.hpp"
#include "ObjectsModel.hpp"

#include <QLabel>
#include <QStackedWidget>
#include <QTabBar>
#include <QTabWidget>
#include <QVBoxLayout>

namespace iprm {

ObjectsView::ObjectsView(QWidget* parent) : QWidget(parent) {
  auto main_layout = new QVBoxLayout(this);
  main_layout->setContentsMargins(0, 0, 0, 0);

  no_object_view_ = new QWidget(this);
  auto no_object_layout = new QVBoxLayout(no_object_view_);
  no_object_layout->setAlignment(Qt::AlignCenter);
  no_object_layout->addWidget(new QLabel(tr("Select an Object")));

  object_view_ = new QTabWidget(this);
  object_view_->setContentsMargins(0, 0, 0, 0);
  object_view_->setTabPosition(QTabWidget::North);
  object_view_->setMovable(true);
  object_view_->setTabsClosable(true);

  connect(object_view_, &QTabWidget::tabCloseRequested, this,
          &ObjectsView::on_object_tab_closed);

  view_ = new QStackedWidget(this);
  view_->addWidget(no_object_view_);
  view_->addWidget(object_view_);
  view_->setCurrentWidget(no_object_view_);

  main_layout->addWidget(view_);
}

void ObjectsView::show(ObjectNodeEntry& object) {
  auto objects_itr = object_views_.find(object.name);
  if (objects_itr != object_views_.end()) {
    object_view_->setCurrentWidget(objects_itr.value());
  } else {
    auto object_view = new ObjectView(object);
    object_view_->addTab(
        object_view, AssetCache::colour_icon(object.hex_colour), object.name);
    object_view_->setCurrentWidget(object_view);
    object_views_[object.name] = object_view;
    object_nodes_[object.name] = &object;
  }
  view_->setCurrentWidget(object_view_);
}

void ObjectsView::on_object_tab_closed(const int tab_index) {
  const auto object_name = object_view_->tabBar()->tabText(tab_index);
  object_views_.remove(object_name);
  object_nodes_.remove(object_name);
  auto object_view = qobject_cast<QWidget*>(object_view_->widget(tab_index));
  object_view_->removeTab(tab_index);
  object_view->deleteLater();
  if (object_view_->count() == 0) {
    view_->setCurrentWidget(no_object_view_);
  }
}

}  // namespace iprm
