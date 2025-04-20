/*
 * Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>
 *
 * SPDX-License-Identifier: MIT
 */
#include "DependencyGraphEdge.hpp"
#include "../util/AppTheme.hpp"

#include <QPainter>

namespace iprm {

DependencyGraphEdge::DependencyGraphEdge(const gv::EdgeItem& edge,
                                         DependencyGraphNode* source_node,
                                         DependencyGraphNode* target_node,
                                         QGraphicsItem* parent)
    : QGraphicsItem(parent),
      source_id_(edge.source_id),
      source_node_(source_node),
      target_id_(edge.target_id),
      target_node_(target_node) {
  if (!source_node_ || !target_node_) {
    qWarning() << "Edge created with invalid source or target node IDs";
    return;
  }

  for (const auto& spline : edge.splines) {
    spline_points_.push_back(QPointF(spline.x, spline.y));
  }

  // Set item position to (0,0) since we're working in scene coordinates
  setPos(0, 0);
}

QRectF DependencyGraphEdge::boundingRect() const {
  if (spline_points_.empty()) {
    return QRectF();
  }

  qreal minX = spline_points_[0].x();
  qreal minY = spline_points_[0].y();
  qreal maxX = spline_points_[0].x();
  qreal maxY = spline_points_[0].y();

  for (const QPointF& p : spline_points_) {
    minX = qMin(minX, p.x());
    minY = qMin(minY, p.y());
    maxX = qMax(maxX, p.x());
    maxY = qMax(maxY, p.y());
  }

  // Add margin for arrow head and stroke width
  return QRectF(minX - 15, minY - 15, maxX - minX + 30, maxY - minY + 30);
}
void DependencyGraphEdge::paint(QPainter* painter,
                                const QStyleOptionGraphicsItem* option,
                                QWidget* widget) {
  Q_UNUSED(option);
  Q_UNUSED(widget);

  if (spline_points_.size() < 2 || !source_node_ || !target_node_) {
    return;
  }

  QPen edgePen(AppTheme::instance().system_colour(), 1.5, Qt::SolidLine, Qt::RoundCap);
  painter->setPen(edgePen);

  QPainterPath path;
  path.moveTo(spline_points_[0]);

  // If we have a Bézier curve (GraphViz typically provides 4 points per
  // segment)
  if (spline_points_.size() == 4) {
    path.cubicTo(spline_points_[1], spline_points_[2], spline_points_[3]);
  }
  // Handle case where we have multiple segments in a spline
  else if (spline_points_.size() > 4) {
    for (int i = 1; i < spline_points_.size(); i += 3) {
      if (i + 2 < spline_points_.size()) {
        path.cubicTo(spline_points_[i], spline_points_[i + 1],
                     spline_points_[i + 2]);
      } else {
        // Not enough points for a full cubic, just line to the end
        path.lineTo(spline_points_[spline_points_.size() - 1]);
      }
    }
  } else {
    for (int i = 1; i < spline_points_.size(); ++i) {
      path.lineTo(spline_points_[i]);
    }
  }

  painter->drawPath(path);

  QPointF last_point = spline_points_.back();
  QPointF second_last_point;

  if (spline_points_.size() >= 2) {
    second_last_point = spline_points_[spline_points_.size() - 2];
  } else {
    second_last_point = last_point - QPointF(10, 0);  // Fallback
  }

  QPointF dir = last_point - second_last_point;
  qreal length = qSqrt(dir.x() * dir.x() + dir.y() * dir.y());

  if (length > 0.001) {
    dir = QPointF(dir.x() / length, dir.y() / length);
  } else {
    dir = QPointF(1.0, 0.0);
  }

  QPointF head_base = last_point;
  // The tip should be a short distance further in the same direction. Not 100%
  // spot on, but close/good enough without having to do any complex/expensive
  // intersection calculations
  QPointF head_tip = head_base + (dir * 10.0);
  draw_arrow_head(painter, head_tip, head_base);
}

void DependencyGraphEdge::draw_arrow_head(QPainter* painter,
                                          const QPointF& tip,
                                          const QPointF& control) {
  qreal dx = tip.x() - control.x();
  qreal dy = tip.y() - control.y();

  qreal length = qSqrt(dx * dx + dy * dy);
  qreal nx, ny;

  if (length > 0.001) {
    nx = dx / length;
    ny = dy / length;
  } else {
    // Default direction if vectors are too close
    nx = 0.0;
    ny = -1.0;
  }

  qreal arrowLength = 10.0;
  qreal arrowWidth = 6.0;

  qreal baseX = tip.x() - nx * arrowLength;
  qreal baseY = tip.y() - ny * arrowLength;

  qreal perpX = -ny;
  qreal perpY = nx;

  qreal leftX = baseX + perpX * arrowWidth / 2.0;
  qreal leftY = baseY + perpY * arrowWidth / 2.0;

  qreal rightX = baseX - perpX * arrowWidth / 2.0;
  qreal rightY = baseY - perpY * arrowWidth / 2.0;

  QPolygonF arrowHead;
  arrowHead << tip << QPointF(leftX, leftY) << QPointF(rightX, rightY);

  painter->setBrush(AppTheme::instance().system_colour());
  painter->setPen(Qt::NoPen);
  painter->drawPolygon(arrowHead);
}

}  // namespace iprm
