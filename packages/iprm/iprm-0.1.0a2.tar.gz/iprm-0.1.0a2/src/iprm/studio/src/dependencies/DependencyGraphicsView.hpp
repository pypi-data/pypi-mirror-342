/*
 * Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>
 *
 * SPDX-License-Identifier: MIT
 */
#pragma once

#include <QGestureEvent>
#include <QGraphicsView>
#include <QPinchGesture>

namespace iprm {

class DependencyGraphNodeSummary;

class DependencyGraphicsView final : public QGraphicsView {
  Q_OBJECT
 public:
  explicit DependencyGraphicsView(QWidget* parent = nullptr);

 Q_SIGNALS:
  void viewport_changed();

 protected:
  bool event(QEvent* event) override;
  void showEvent(QShowEvent* event) override;
  void hideEvent(QHideEvent* event) override;
  void resizeEvent(QResizeEvent* event) override;
  void wheelEvent(QWheelEvent* event) override;
  void mousePressEvent(QMouseEvent* event) override;
  void mouseReleaseEvent(QMouseEvent* event) override;
  void mouseMoveEvent(QMouseEvent* event) override;
  bool gestureEvent(QGestureEvent* event);
  void pinchTriggered(QPinchGesture* gesture);

 private:
  bool first_show_{true};
  bool panning_{false};
  qreal current_scale_ = 1.0;
  QPoint last_mouse_pos_;
  const qreal zoom_factor_{1.15};
  DependencyGraphNodeSummary* node_summary_{nullptr};
};

}  // namespace iprm
