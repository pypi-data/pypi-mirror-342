/*
 * Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>
 *
 * SPDX-License-Identifier: MIT
 */
#pragma once

#include "../../../core/src/TypeFlags.hpp"

#include <QComboBox>
#include <QHash>
#include <QWidget>

class QStackedWidget;
class QTabWidget;
class QHBoxLayout;

namespace iprm {

class ObjectNodeEntry;

class ObjectPropertiesView : public QWidget {
  Q_OBJECT
 public:
  // TODO: Should be initialized with all possible platforms so the platforms
  //  view has selection for all, will be passed from
  //  ObjectsView -> FIleView -> Project -> MainWindow -> APIBridge
  explicit ObjectPropertiesView(QWidget* parent = nullptr);

  void show(ObjectNodeEntry& object);

 private Q_SLOTS:
  void on_object_tab_closed(int tab_index);

  void on_edit_platforms();

 private:
  enum Role { PlatformNameRole = Qt::UserRole + 1 };


  QWidget* make_view(ObjectNodeEntry& object);

  QHBoxLayout* make_name_view(const QString& name,
                              const QString& hex_colour,
                              const QStringList& platforms);

  QHBoxLayout* make_type_view(const QString& type_name, TypeFlags type_flags);

  QHBoxLayout* make_platforms_view(const QStringList& platforms);

  // TODO: for all the other built-in/known properties, have dedicated methods.
  // Then for the remaining that depend on the type, just have
  // "make_property_view()" which will take in the info exposed on the python
  // side, which specifies:
  //  - The type of editable widget to create (just an enum that we will map to
  //  a Qt type)
  //  - The value of the label/prompt
  //  - The value of the property that we will populate the view with
  //  - The initially supported list of platform names

  QStackedWidget* view_{nullptr};
  QWidget* no_object_view_{nullptr};
  QTabWidget* object_view_{nullptr};
  QHash<QString, QWidget*> object_views_;
  QHash<QString, ObjectNodeEntry*> object_nodes_;
  QStringList platforms_;
};

class ObjectTypeComboBox : public QComboBox {
  Q_OBJECT
 public:
  explicit ObjectTypeComboBox(QWidget* parent = nullptr);

  void setIndex(const QModelIndex& type_index);

protected:
  void showPopup() override;

 private Q_SLOTS:
  void prepare_popup();

  void on_item_activated(const QModelIndex& type_index);

 private:
  QPersistentModelIndex type_index_;
};

}  // namespace iprm
