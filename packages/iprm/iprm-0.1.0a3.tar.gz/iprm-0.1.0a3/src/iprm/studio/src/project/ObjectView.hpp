/*
 * Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>
 *
 * SPDX-License-Identifier: MIT
 */
#pragma once

#include "../../../core/src/TypeFlags.hpp"

#include <QScrollArea>

class QHBoxLayout;

namespace iprm {

class Object;
class ObjectNodeEntry;

class ObjectView : public QScrollArea {
  Q_OBJECT
 public:
  explicit ObjectView(ObjectNodeEntry& object, QWidget* parent = nullptr);

 Q_SIGNALS:
  void type_changed(qlonglong type_flags_underlying);

 private Q_SLOTS:
  void on_edit_platforms();

 private:
  enum Role { PlatformNameRole = Qt::UserRole + 1 };

  QHBoxLayout* make_name_view(const QString& name, const QString& hex_colour);

  QHBoxLayout* make_type_view(const QString& type_name, TypeFlags type_flags);

  QWidget* make_properties_view(
      const QHash<QString, QPair<QIcon, Object>>& platform_objects,
      TypeFlags type_flags);

  QHBoxLayout* make_platforms_view(const QStringList& platforms);

  ObjectNodeEntry& object_;
  QStringList platforms_;
  QHash<TypeFlags, QWidget*> object_properties_views_;
};

}  // namespace iprm
