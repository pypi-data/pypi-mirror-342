/*
 * Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>
 *
 * SPDX-License-Identifier: MIT
 */
#pragma once

#include "../util/APIBridge.hpp"

#include <QScrollArea>

class QStackedWidget;
class QTabWidget;

namespace iprm {

namespace gv {
struct LayoutResult;
}  // namespace gv

class LoadingWidget;
class DependencyGraphicsView;
class DependencyGraphicsScene;

class DependencyView final : public QScrollArea {
  Q_OBJECT
 public:
  explicit DependencyView(QWidget* parent = nullptr);

  void build_graph(const QString& platform_display_name,
                   const QIcon& platform_icon,
                   const gv::LayoutResult& graph_layout);

  void load_graphs() const;

  void show_graphs(const QString& host_platform_display_name) const;

 private:
  QStackedWidget* stack_{nullptr};
  LoadingWidget* loading_page_{nullptr};
  QHash<QString, DependencyGraphicsView*> views_;
  QHash<QString, DependencyGraphicsScene*> scenes_;

  QTabWidget* platforms_{nullptr};
};

}  // namespace iprm
