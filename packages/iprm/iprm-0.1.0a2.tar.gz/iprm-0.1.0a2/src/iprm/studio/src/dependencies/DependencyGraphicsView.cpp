/*
 * Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>
 *
 * SPDX-License-Identifier: MIT
 */

#include "DependencyGraphicsView.hpp"
#include "DependencyGraphItemFactory.hpp"
#include "DependencyGraphNodeSummary.hpp"
#include "DependencyGraphicsScene.hpp"
#include "DependencyGraphNode.hpp"

#include <QScrollBar>
#include <QTimer>
#include <QGuiApplication>

namespace iprm {

DependencyGraphicsView::DependencyGraphicsView(QWidget* parent)
    : QGraphicsView(parent),
      node_summary_(new DependencyGraphNodeSummary(*this)) {
  setRenderHint(QPainter::Antialiasing);
  setViewportUpdateMode(FullViewportUpdate);
  setHorizontalScrollBarPolicy(Qt::ScrollBarAsNeeded);
  setVerticalScrollBarPolicy(Qt::ScrollBarAsNeeded);
  setDragMode(RubberBandDrag);

  setAttribute(Qt::WA_AcceptTouchEvents);
  grabGesture(Qt::PinchGesture);
  viewport()->setAttribute(Qt::WA_AcceptTouchEvents);
}

bool DependencyGraphicsView::event(QEvent* event) {
  if (event->type() == QEvent::Gesture) {
    return gestureEvent(dynamic_cast<QGestureEvent*>(event));
  }
  return QGraphicsView::event(event);
}

void DependencyGraphicsView::showEvent(QShowEvent* event) {
  QGraphicsView::showEvent(event);
  if (event->spontaneous() || !first_show_) {
    return;
  }
  first_show_ = false;
  QTimer::singleShot(0, this, [this]() {
    auto dep_scene = qobject_cast<DependencyGraphicsScene*>(scene());
    if (dep_scene == nullptr) {
      return;
    }

    QRectF itemsRect = dep_scene->itemsBoundingRect();
    if (itemsRect.isEmpty()) {
      return;
    }

    static constexpr qreal margin = 0.2;
    QRectF expandedRect = itemsRect.adjusted(
        -itemsRect.width() * margin, -itemsRect.height() * margin,
        itemsRect.width() * margin, itemsRect.height() * margin);

    dep_scene->setSceneRect(expandedRect);
    fitInView(expandedRect, Qt::KeepAspectRatio);
    viewport()->update();

    dep_scene->addItem(node_summary_);
    connect(dep_scene->item_factory(),
            &DependencyGraphItemFactory::node_hover_state_changed,
            node_summary_, &DependencyGraphNodeSummary::on_hover_state_changed);
    node_summary_->update_position();
  });
}

void DependencyGraphicsView::hideEvent(QHideEvent* event) {
  QGraphicsView::hideEvent(event);
  unsetCursor();
}

void DependencyGraphicsView::resizeEvent(QResizeEvent* event) {
  QGraphicsView::resizeEvent(event);
  Q_EMIT viewport_changed();
}

void DependencyGraphicsView::wheelEvent(QWheelEvent* event) {
  bool from_trackpad = (event->source() == Qt::MouseEventSynthesizedBySystem);
  if (!from_trackpad) {
    QPointF scene_pos = mapToScene(event->position().toPoint());
    qreal factor =
        event->angleDelta().y() > 0 ? zoom_factor_ : 1.0 / zoom_factor_;
    scale(factor, factor);
    QPointF delta = mapToScene(event->position().toPoint()) - scene_pos;
    translate(delta.x(), delta.y());
  } else {
    QPoint pixels = event->pixelDelta();
    QPoint degrees = event->angleDelta() / 8;

    // Use pixel delta for smoother scrolling if available
    if (!pixels.isNull()) {
      horizontalScrollBar()->setValue(horizontalScrollBar()->value() -
                                      pixels.x());
      verticalScrollBar()->setValue(verticalScrollBar()->value() - pixels.y());
    } else if (!degrees.isNull()) {
      QPoint steps = degrees / 15;
      horizontalScrollBar()->setValue(horizontalScrollBar()->value() -
                                      steps.x() * 20);
      verticalScrollBar()->setValue(verticalScrollBar()->value() -
                                    steps.y() * 20);
    }
  }
  Q_EMIT viewport_changed();
  event->accept();
}

bool DependencyGraphicsView::gestureEvent(QGestureEvent* event) {
  if (QGesture* pinch = event->gesture(Qt::PinchGesture)) {
    pinchTriggered(dynamic_cast<QPinchGesture*>(pinch));
    return true;
  }
  return false;
}

void DependencyGraphicsView::pinchTriggered(QPinchGesture* gesture) {
  QPinchGesture::ChangeFlags changeFlags = gesture->changeFlags();

  if (changeFlags & QPinchGesture::ScaleFactorChanged) {
    QPointF center = gesture->centerPoint();

    QPointF scene_pos = mapToScene(center.toPoint());

    qreal scale_factor = gesture->scaleFactor();

    // Avoid excessive scaling from single gestures
    if (scale_factor > 2.0)
      scale_factor = 2.0;
    if (scale_factor < 0.5)
      scale_factor = 0.5;

    scale(scale_factor, scale_factor);
    current_scale_ *= scale_factor;

    QPointF delta = mapToScene(center.toPoint()) - scene_pos;
    translate(delta.x(), delta.y());
    Q_EMIT viewport_changed();
  }
}

void DependencyGraphicsView::mousePressEvent(QMouseEvent* event) {
  if (event->button() == Qt::LeftButton) {
    panning_ = true;
    last_mouse_pos_ = event->pos();
    setCursor(Qt::ClosedHandCursor);
    event->accept();
  } else {
    QGraphicsView::mousePressEvent(event);
  }
}

void DependencyGraphicsView::mouseReleaseEvent(QMouseEvent* event) {
  if (event->button() == Qt::LeftButton) {
    panning_ = false;
    unsetCursor();
    event->accept();
  } else {
    QGraphicsView::mouseReleaseEvent(event);
  }
}

void DependencyGraphicsView::mouseMoveEvent(QMouseEvent* event) {
  if (panning_) {
    QPoint delta = event->pos() - last_mouse_pos_;
    last_mouse_pos_ = event->pos();
    horizontalScrollBar()->setValue(horizontalScrollBar()->value() - delta.x());
    verticalScrollBar()->setValue(verticalScrollBar()->value() - delta.y());
    Q_EMIT viewport_changed();
    event->accept();
  } else {
    QGraphicsView::mouseMoveEvent(event);
  }
}

}  // namespace iprm
