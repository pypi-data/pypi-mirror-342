/*
 * Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>
 *
 * SPDX-License-Identifier: MIT
 */
#include "ObjectsModel.hpp"
#include "../util/AssetCache.hpp"

#include <QPainter>

#include <ranges>

namespace iprm {

ObjectsModel::ObjectsModel(QObject* parent) : QAbstractItemModel(parent) {
  qRegisterMetaType<QList<QIcon>>();
  qRegisterMetaType<ObjectNodeEntry>();
}

void ObjectsModel::load(const QHash<QString, PlatformFile>& file) {
  beginResetModel();
  QHash<QString, ObjectNodeEntry> entries;

  QHashIterator file_itr(file);

  auto platform_names = file.keys();
  std::ranges::sort(platform_names);

  for (const auto& platform_name : platform_names) {
    const auto& platform_file = file[platform_name];

    const auto& platform_icon = platform_file.icon_;
    const auto& platform_objects = platform_file.objects_;
    for (const auto& object : platform_objects) {
      const QString unique_entry_key =
          QString("%0/%1").arg(object.name, object.type_name);
      auto entry_itr = entries.find(unique_entry_key);
      if (entry_itr != entries.end()) {
        entry_itr.value().platform_objects_.insert(platform_name, object);
      } else {
        entries[unique_entry_key] = ObjectNodeEntry{
            .name = object.name,
            .type_name = object.type_name,
            .type = object.type,
            .hex_colour = object.hex_colour,
            .compiler_version =
                object.properties["compiler_version"].toString(),
            .icon = object.icon.has_value()
                        ? object.icon.value()
                        : AssetCache::object_type_icon(object.type),
            .platform_objects_ = {{platform_name, object}}};
      }
    }
  }

  objects_ = entries.values();
  endResetModel();
}

ObjectNodeEntry& ObjectsModel::get_object_node(const QModelIndex& index) {
  assert(index.row() < objects_.size());
  return objects_[index.row()];
}

QVariant ObjectsModel::data(const QModelIndex& index, int role) const {
  if (!index.isValid()) {
    return QModelIndex();
  }
  const int row = index.row();
  const int column = index.column();

  const ObjectNodeEntry& obj_entry = objects_[row];

  switch (role) {
    case Qt::DisplayRole: {
      if (column == 0) {
        if (static_cast<bool>(obj_entry.type & TypeFlags::SUBDIR)) {
          return QString("<iprm_subdir>");
        }
        return obj_entry.name;
      } else if (column == 1) {
        return obj_entry.type_name;
      }
    }
    case ObjectNameIconsRole: {
      if (column == 0) {
        QList object_icons{AssetCache::colour_icon(obj_entry.hex_colour)};
        for (const auto& platform_name : obj_entry.platform_objects_.keys()) {
          object_icons.append(AssetCache::platform_icon(platform_name));
        }
        return QVariant::fromValue(object_icons);
      }
    }
    case Qt::DecorationRole: {
      if (column == 1) {
        return obj_entry.icon;
      }
    }
    case Qt::ToolTipRole: {
      // TODO: Just display the name of the compiler, not the version info
      return obj_entry.compiler_version;
    }
    default:
      break;
  }

  return QVariant{};
}

QVariant ObjectsModel::headerData(int section,
                                  Qt::Orientation orientation,
                                  int role) const {
  if (orientation == Qt::Horizontal && role == Qt::DisplayRole) {
    static const QStringList headers{tr("Name"), tr("Type")};
    return headers[section];
  }
  return QVariant{};
}

int ObjectsModel::columnCount(const QModelIndex&) const {
  // Name, Type
  return 2;
}

QModelIndex ObjectsModel::index(int row,
                                int column,
                                const QModelIndex& parent) const {
  if (row < 0 || column < 0 || row >= rowCount(parent) ||
      column >= columnCount(parent)) {
    return QModelIndex{};
  }
  return createIndex(row, column, &objects_.at(row));
}

QModelIndex ObjectsModel::parent(const QModelIndex&) const {
  // We tabular
  return QModelIndex{};
}

int ObjectsModel::rowCount(const QModelIndex&) const {
  return static_cast<int>(objects_.size());
}

ObjectsSortFilterProxyModel::ObjectsSortFilterProxyModel(QObject* parent)
    : QSortFilterProxyModel(parent) {}

bool ObjectsSortFilterProxyModel::lessThan(const QModelIndex& left,
                                           const QModelIndex& right) const {
  const auto left_entry =
      static_cast<const ObjectNodeEntry*>(left.internalPointer());
  const auto right_entry =
      static_cast<const ObjectNodeEntry*>(right.internalPointer());

  if (!left_entry || !right_entry) {
    return QSortFilterProxyModel::lessThan(left, right);
  }

  const bool left_is_project =
      static_cast<bool>(left_entry->type & TypeFlags::PROJECT);
  const bool right_is_project =
      static_cast<bool>(right_entry->type & TypeFlags::PROJECT);

  if (left_is_project && !right_is_project) {
    return true;
  } else if (!left_is_project && right_is_project) {
    return false;
  } else {
    return QSortFilterProxyModel::lessThan(left, right);
  }
}

}  // namespace iprm
