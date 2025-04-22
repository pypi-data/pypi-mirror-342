/*
 * Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>
 *
 * SPDX-License-Identifier: MIT
 */
#include "DependencyView.hpp"
#include "../util/LoadingWidget.hpp"
#include "DependencyGraphicsScene.hpp"
#include "DependencyGraphicsView.hpp"

#include <QStackedWidget>
#include <QTableWidget>

namespace iprm {

DependencyView::DependencyView(QWidget* parent) : QScrollArea(parent) {
  setWidgetResizable(true);
  setHorizontalScrollBarPolicy(Qt::ScrollBarAsNeeded);
  setVerticalScrollBarPolicy(Qt::ScrollBarAsNeeded);

  stack_ = new QStackedWidget(this);
  setWidget(stack_);

  loading_page_ = new LoadingWidget(this);
  loading_page_->set_text(tr("Generating graph..."));

  platforms_ = new QTabWidget(this);
  platforms_->setMovable(true);

  auto blank = new QWidget();
  stack_->addWidget(blank);
  stack_->addWidget(loading_page_);
  stack_->addWidget(platforms_);
  stack_->setCurrentWidget(blank);
}

void DependencyView::build_graph(const QString& platform_display_name,
                                 const QIcon& platform_icon,
                                 const gv::LayoutResult& graph_layout) {
  DependencyGraphicsView* view = [this, &platform_display_name]() {
    auto views_itr = views_.find(platform_display_name);
    if (views_itr == views_.end()) {
      auto view = new DependencyGraphicsView(this);
      views_[platform_display_name] = view;
      return view;
    }
    return views_itr.value();
  }();

  DependencyGraphicsScene* scene = [this, &platform_display_name]() {
    auto scene_itr = scenes_.find(platform_display_name);
    if (scene_itr == scenes_.end()) {
      auto scene = new DependencyGraphicsScene(this);
      scenes_[platform_display_name] = scene;
      return scene;
    }
    return scene_itr.value();
  }();

  view->setScene(scene);

  platforms_->addTab(view, platform_icon, platform_display_name);
  scene->build_graph(graph_layout);
}

void DependencyView::load_graphs() const {
  stack_->setCurrentWidget(loading_page_);
}

void DependencyView::show_graphs(
    const QString& host_platform_display_name) const {
  assert(views_.contains(host_platform_display_name));
  platforms_->setCurrentWidget(views_[host_platform_display_name]);
  stack_->setCurrentWidget(platforms_);
}

}  // namespace iprm
