/*
 * Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>
 *
 * SPDX-License-Identifier: MIT
 */
#pragma once

#include "../util/graphviz.hpp"
#include <QGraphicsItem>

namespace iprm {

class DependencyGraphNode;

class DependencyGraphEdge : public QGraphicsItem {
 public:
  DependencyGraphEdge(const gv::EdgeItem& edge,
                      DependencyGraphNode* source_node,
                      DependencyGraphNode* target_node,
                      QGraphicsItem* parent = nullptr);

  QRectF boundingRect() const override;

  void paint(QPainter* painter,
             const QStyleOptionGraphicsItem* option,
             QWidget* widget) override;

 private:
  void draw_arrow_head(QPainter* painter,
                       const QPointF& tip,
                       const QPointF& control);
  int source_id_;
  DependencyGraphNode* source_node_;
  int target_id_;
  DependencyGraphNode* target_node_;
  std::vector<QPointF> spline_points_;
};

}  // namespace iprm
