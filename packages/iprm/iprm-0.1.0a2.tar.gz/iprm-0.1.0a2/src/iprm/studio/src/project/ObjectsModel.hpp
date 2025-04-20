/*
 * Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>
 *
 * SPDX-License-Identifier: MIT
 */
#pragma once

#include "../util/APIBridge.hpp"

#include <QAbstractItemModel>
#include <QIcon>
#include <QMetaType>
#include <QSortFilterProxyModel>

namespace iprm {

enum Role { ObjectNameIconsRole = Qt::UserRole + 1 };

struct ObjectNodeEntry {
  QString name;
  QString type_name;
  TypeFlags type;
  QString hex_colour;
  QString compiler_version;
  QIcon icon;
  QHash<QString, ObjectNode> platform_objects_;
};

class ObjectsModel : public QAbstractItemModel {
  Q_OBJECT
 public:
  ObjectsModel(QObject* parent = nullptr);

  void load(const QHash<QString, PlatformFile>& file);

  [[nodiscard]] ObjectNodeEntry& get_object_node(
      const QModelIndex& index);

 protected:
  [[nodiscard]] int columnCount(const QModelIndex& parent) const override;

  [[nodiscard]] QVariant data(const QModelIndex& index,
                              int role) const override;

  [[nodiscard]] QVariant headerData(int section,
                                    Qt::Orientation orientation,
                                    int role) const override;
  [[nodiscard]] QModelIndex index(int row,
                                  int column,
                                  const QModelIndex& parent) const override;

  [[nodiscard]] QModelIndex parent(const QModelIndex& index) const override;

  [[nodiscard]] int rowCount(const QModelIndex& parent) const override;

 private:
  QList<ObjectNodeEntry> objects_;
};

class ObjectsSortFilterProxyModel : public QSortFilterProxyModel {
  Q_OBJECT
 public:
  explicit ObjectsSortFilterProxyModel(QObject* parent = nullptr);

 protected:
  bool lessThan(const QModelIndex& left,
                const QModelIndex& right) const override;
};

}  // namespace iprm

Q_DECLARE_METATYPE(QList<QIcon>)
Q_DECLARE_METATYPE(iprm::ObjectNodeEntry)
