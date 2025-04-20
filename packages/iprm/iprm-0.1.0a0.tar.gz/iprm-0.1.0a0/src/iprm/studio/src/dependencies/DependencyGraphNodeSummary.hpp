/*
 * Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>
 *
 * SPDX-License-Identifier: MIT
 */
#pragma once

#include <QGraphicsProxyWidget>

class QStackedWidget;

namespace iprm {

class DependencyGraphicsView;
class DependencyGraphNode;

class DependencyGraphNodeSummary : public QGraphicsProxyWidget {
  Q_OBJECT
 public:
  DependencyGraphNodeSummary(DependencyGraphicsView& graphics_view);

 public Q_SLOTS:
  void update_position();

  void on_hover_state_changed(DependencyGraphNode* node, bool hovering);

 private:
  DependencyGraphicsView& graphics_view_;
  QStackedWidget* summary_view_{nullptr};
  std::unordered_map<int, QWidget*> summaries_;
};

}  // namespace iprm
