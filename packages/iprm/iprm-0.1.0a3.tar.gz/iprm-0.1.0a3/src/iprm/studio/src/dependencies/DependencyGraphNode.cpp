/*
 * Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>
 *
 * SPDX-License-Identifier: MIT
 */
#include "DependencyGraphNode.hpp"
#include "../util/AppTheme.hpp"

#include <QCursor>
#include <QGraphicsSceneHoverEvent>
#include <QPainter>

namespace iprm {
namespace {
QPainterPath create_ellipse(qreal width, qreal height) {
  QPainterPath path;

  qreal rx = width / 2.0;
  qreal ry = height / 2.0;

  // Magic constant for a close approximation of an ellipse using Bezier
  // curves
  qreal c = 0.551915024494;

  // Top point
  path.moveTo(0, -ry);

  // Right curve
  path.cubicTo(c * rx, -ry, rx, -c * ry, rx, 0);

  // Bottom curve
  path.cubicTo(rx, c * ry, c * rx, ry, 0, ry);

  // Left curve
  path.cubicTo(-c * rx, ry, -rx, c * ry, -rx, 0);

  // Top curve
  path.cubicTo(-rx, -c * ry, -c * rx, -ry, 0, -ry);

  return path;
}

QColor hex_to_colour(const QString& hex) {
  QString cleanHex = hex;
  if (cleanHex.startsWith('#')) {
    cleanHex = cleanHex.mid(1);
  }

  if (cleanHex.length() != 6) {
    return QColor(Qt::gray);  // Default color on error
  }

  bool ok;
  int r = cleanHex.mid(0, 2).toInt(&ok, 16);
  if (!ok)
    return QColor(Qt::gray);

  int g = cleanHex.mid(2, 2).toInt(&ok, 16);
  if (!ok)
    return QColor(Qt::gray);

  int b = cleanHex.mid(4, 2).toInt(&ok, 16);
  if (!ok)
    return QColor(Qt::gray);

  return QColor(r, g, b);
}
}  // namespace

void NodeStateChangeNotifier::notify_state_changed(int node_id, bool hovering) {
  Q_EMIT hover_state_changed(node_id, hovering);
}

DependencyGraphNode::DependencyGraphNode(const gv::NodeItem& node,
                                         QGraphicsItem* parent)
    : QGraphicsItem(parent),
      m_id(node.id),
      name_(QString::fromStdString(node.name)),
      target_type_(QString::fromStdString(node.target_type)),
      type_flags_(node.type),
      icon_(node.icon),
      shape_type_(QString::fromStdString(node.shape_type)),
      hex_colour_(QString::fromStdString(node.hex_colour)),
      obj_project_rel_dir_path_(
          QString::fromStdString(node.obj_project_rel_dir_path)),
      x_(node.x),
      y_(node.y),
      width_(node.width),
      height_(node.height) {
  setPos(x_, y_);

  setAcceptHoverEvents(true);
}

QPainterPath DependencyGraphNode::node_path() const {
  QPainterPath path;

  if (shape_type_ == "circle") {
    qreal radius = qMin(width_, height_) / 2.0;
    path.addEllipse(-radius, -radius, radius * 2, radius * 2);
  } else if (shape_type_ == "ellipse") {
    path = create_ellipse(width_, height_);
  } else if (shape_type_ == "diamond") {
    path.moveTo(-width_ / 2.0, 0);
    path.lineTo(0, -height_ / 2.0);
    path.lineTo(width_ / 2.0, 0);
    path.lineTo(0, height_ / 2.0);
    path.closeSubpath();
  } else if (shape_type_ == "rectangle") {
    path.addRect(-width_ / 2.0, -height_ / 2.0, width_, height_);
  } else {
    // Default to circle for unknown shapes
    qreal radius = qMin(width_, height_) / 2.0;
    path.addEllipse(-radius, -radius, radius * 2, radius * 2);
  }

  return path;
}

QRectF DependencyGraphNode::boundingRect() const {
  return QRectF(-width_ / 2 - 2, -height_ / 2 - 2, width_ + 4, height_ + 4);
}

void DependencyGraphNode::hoverEnterEvent(QGraphicsSceneHoverEvent* event) {
  const QPointF pos = event->pos();
  if (node_path().contains(pos)) {
    hovering_ = true;
    setCursor(Qt::PointingHandCursor);
    state_change_nofifier_.notify_state_changed(id(), hovering_);
    update();
  }
  QGraphicsItem::hoverEnterEvent(event);
}

void DependencyGraphNode::hoverMoveEvent(QGraphicsSceneHoverEvent* event) {
  const QPointF pos = event->pos();
  const bool was_hovering = hovering_;
  hovering_ = node_path().contains(pos);
  if (was_hovering != hovering_) {
    if (hovering_) {
      setCursor(Qt::PointingHandCursor);
    } else {
      unsetCursor();
    }
    state_change_nofifier_.notify_state_changed(id(), hovering_);
    update();
  }
  QGraphicsItem::hoverMoveEvent(event);
}

void DependencyGraphNode::hoverLeaveEvent(QGraphicsSceneHoverEvent* event) {
  hovering_ = false;
  unsetCursor();
  state_change_nofifier_.notify_state_changed(id(), hovering_);
  update();
  QGraphicsItem::hoverLeaveEvent(event);
}

void DependencyGraphNode::paint(QPainter* painter,
                                const QStyleOptionGraphicsItem* option,
                                QWidget* widget) {
  Q_UNUSED(option);
  Q_UNUSED(widget);

  QPainterPath path = node_path();

  const QColor nodeColor = hex_to_colour(hex_colour_);
  painter->fillPath(path, nodeColor);
  painter->strokePath(path, QPen(AppTheme::instance().system_colour()));

  if (hovering_) {
    QPen highlightPen(QColor("#00B3C7"));
    highlightPen.setWidth(2);
    painter->setPen(highlightPen);
    painter->drawPath(path);
  }

  painter->setPen(AppTheme::instance().system_colour());
  painter->setFont(QFont("Arial", 10));

  QRectF textRect = boundingRect();
  painter->drawText(textRect, Qt::AlignCenter, name_);
}

}  // namespace iprm
