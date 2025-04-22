/*
 * Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>
 *
 * SPDX-License-Identifier: MIT
 */
#pragma once

#include "../util/graphviz.hpp"

#include <QGraphicsItem>

namespace iprm {

class NodeStateChangeNotifier : public QObject {
  Q_OBJECT
 public:
  void notify_state_changed(int node_id, bool hovering);

 Q_SIGNALS:
  void hover_state_changed(int node_id, bool hovering);
};

class DependencyGraphNode : public QGraphicsItem {
 public:
  DependencyGraphNode(const gv::NodeItem& node,
                      QGraphicsItem* parent = nullptr);

  QPainterPath node_path() const;

  QPointF calculate_shape_intersection(qreal nx, qreal ny) const;

  QRectF boundingRect() const override;

  void paint(QPainter* painter,
             const QStyleOptionGraphicsItem* option,
             QWidget* widget) override;

  qreal x() const { return x_; }
  qreal y() const { return y_; }
  qreal width() const { return width_; }
  qreal height() const { return height_; }
  int id() const { return m_id; }
  const QString& name() const { return name_; }
  const QString& target_type() const { return target_type_; }
  TypeFlags type_flags() const { return type_flags_; }
  const QIcon& icon() const { return icon_; }
  const QString& shape_type() const { return shape_type_; }
  const QString& obj_project_rel_dir_path() const {
    return obj_project_rel_dir_path_;
  }

  NodeStateChangeNotifier& state_change_notifier() {
    return state_change_nofifier_;
  }

 protected:
  void hoverEnterEvent(QGraphicsSceneHoverEvent* event) override;
  void hoverLeaveEvent(QGraphicsSceneHoverEvent* event) override;
  void hoverMoveEvent(QGraphicsSceneHoverEvent* event) override;

 private:
  int m_id;
  QString name_;
  QString target_type_;
  TypeFlags type_flags_;
  QIcon icon_;
  QString shape_type_;
  QString hex_colour_;
  QString obj_project_rel_dir_path_;
  qreal x_;
  qreal y_;
  qreal width_;
  qreal height_;
  bool hovering_{false};
  NodeStateChangeNotifier state_change_nofifier_;
};

}  // namespace iprm
