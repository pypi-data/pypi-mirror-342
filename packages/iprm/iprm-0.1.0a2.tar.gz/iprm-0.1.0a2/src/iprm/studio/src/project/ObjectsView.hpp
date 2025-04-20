/*
 * Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>
 *
 * SPDX-License-Identifier: MIT
 */
#pragma once

#include "../util/APIBridge.hpp"
#include "ObjectsModel.hpp"

#include <QStyledItemDelegate>
#include <QTreeView>

namespace iprm {

class ObjectsView : public QTreeView {
  Q_OBJECT

 public:
  ObjectsView(QWidget* parent = nullptr);

  void load(const QHash<QString, PlatformFile>& file);

 Q_SIGNALS:
  void object_selected(ObjectNodeEntry& object);

 protected:
  void showEvent(QShowEvent* event) override;
  void dragEnterEvent(QDragEnterEvent* event) override;
  void dragMoveEvent(QDragMoveEvent* event) override;
  void dropEvent(QDropEvent* event) override;

 private:
  ObjectsModel* model_{nullptr};
  ObjectsSortFilterProxyModel* proxy_model_{nullptr};
};

class ObjectNameDelegate : public QStyledItemDelegate {
  Q_OBJECT

 public:
  explicit ObjectNameDelegate(QObject* parent = nullptr);

  void paint(QPainter* painter,
             const QStyleOptionViewItem& option,
             const QModelIndex& index) const override;

  QSize sizeHint(const QStyleOptionViewItem& option,
                 const QModelIndex& index) const override;
};

}  // namespace iprm
