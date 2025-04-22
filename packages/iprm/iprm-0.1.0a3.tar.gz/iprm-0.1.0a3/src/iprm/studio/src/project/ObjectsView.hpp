/*
 * Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>
 *
 * SPDX-License-Identifier: MIT
 */
#pragma once

#include <QHash>
#include <QWidget>

class QStackedWidget;
class QTabWidget;
class QHBoxLayout;

namespace iprm {

class Object;
class ObjectNodeEntry;
class ObjectView;

class ObjectsView : public QWidget {
  Q_OBJECT
 public:
  explicit ObjectsView(QWidget* parent = nullptr);

  void show(ObjectNodeEntry& object);

 private Q_SLOTS:
  void on_object_tab_closed(int tab_index);

 private:
  QStackedWidget* view_{nullptr};
  QWidget* no_object_view_{nullptr};
  QTabWidget* object_view_{nullptr};
  QHash<QString, ObjectView*> object_views_;
  QHash<QString, ObjectNodeEntry*> object_nodes_;
};

}  // namespace iprm
