/*
 * Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>
 *
 * SPDX-License-Identifier: MIT
 */
#pragma once

#include "../util/graphviz.hpp"

#include <QObject>

class QGraphicsScene;

namespace iprm {

class DependencyGraphNode;
class DependencyGraphEdge;

class DependencyGraphItemFactory : public QObject {
  Q_OBJECT
 public:
  DependencyGraphItemFactory(QGraphicsScene* scene, QObject* parent = nullptr);

  void create(const gv::LayoutResult& result);

  void clear();

 Q_SIGNALS:
  void node_hover_state_changed(DependencyGraphNode* node, bool hovering);

 private:
  QGraphicsScene* scene_;
  std::unordered_map<int, DependencyGraphNode*> nodes_;
  std::vector<DependencyGraphEdge*> edges_;
};

}  // namespace iprm
