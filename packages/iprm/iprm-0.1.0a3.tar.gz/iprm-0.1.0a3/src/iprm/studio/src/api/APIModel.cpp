/*
 * Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>
 *
 * SPDX-License-Identifier: MIT
 */
#include "APIModel.hpp"
#include "APIItem.hpp"
#include "APIView.hpp"

namespace iprm {

APIModel::APIModel(QObject* parent)
    : QAbstractItemModel(parent),
      root_(std::make_unique<APIItem>("NAMESPACE", APICategoryEntry{})),
      nest_third_party_extensions_(qobject_cast<APIView*>(parent) != nullptr) {}

APIModel::~APIModel() = default;

void APIModel::load(
    const QHash<QString, QHash<QString, APICategoryEntry>>& public_api) {
  beginResetModel();

  APIItem::opt_ref_t cpp_third_party_item_ref;
  std::vector<std::unique_ptr<APIItem>> cpp_third_party_extension_items;

  QHashIterator public_api_itr(public_api);
  while (public_api_itr.hasNext()) {
    public_api_itr.next();
    const auto& category = public_api_itr.key();
    auto category_item =
        std::make_unique<APIItem>(category, APICategoryEntry{}, *root_);

    const QHash<QString, APICategoryEntry>& public_api_category =
        public_api[category];

    QHashIterator public_api_category_itr(public_api_category);
    while (public_api_category_itr.hasNext()) {
      public_api_category_itr.next();

      const QString& entry_name = public_api_category_itr.key();
      const APICategoryEntry& entry_data = public_api_category_itr.value();

      auto child_item =
          std::make_unique<APIItem>(entry_name, entry_data, *category_item);
      if (static_cast<bool>(entry_data.type_ & TypeFlags::THIRDPARTY)) {
        if (entry_name == "CppThirdParty") {
          category_item->append_child(std::move(child_item));
          cpp_third_party_item_ref =
              category_item->child(category_item->child_count() - 1);
          continue;
        } else if (nest_third_party_extensions_) {
          cpp_third_party_extension_items.push_back(std::move(child_item));
          continue;
        }
      }

      category_item->append_child(std::move(child_item));
    }
    root_->append_child(std::move(category_item));
  }

  assert(cpp_third_party_item_ref.has_value());
  auto& cpp_third_party_item = cpp_third_party_item_ref.value().get();
  for (auto&& cpp_third_party_extension_item :
       cpp_third_party_extension_items) {
    cpp_third_party_item.append_child(
        std::move(cpp_third_party_extension_item));
  }

  endResetModel();
}

QVariant APIModel::data(const QModelIndex& index, const int role) const {
  if (!index.isValid()) {
    return QVariant{};
  }
  const auto item = static_cast<APIItem*>(index.internalPointer());
  return item->data(index, role);
}

Qt::ItemFlags APIModel::flags(const QModelIndex& index) const {
  if (!index.isValid()) {
    return Qt::NoItemFlags;
  }

  return QAbstractItemModel::flags(index);
}

QVariant APIModel::headerData(int, Qt::Orientation, int) const {
  return QVariant();
}

QModelIndex APIModel::index(const int row,
                            const int column,
                            const QModelIndex& parent) const {
  if (!hasIndex(row, column, parent)) {
    return QModelIndex();
  }

  APIItem::opt_ref_t parent_item;
  if (!parent.isValid()) {
    parent_item = *root_;
  } else {
    parent_item = *static_cast<APIItem*>(parent.internalPointer());
  }

  if (const APIItem::opt_ref_t child_item =
          parent_item.value().get().child(row)) {
    return createIndex(row, column, &child_item.value().get());
  }
  return QModelIndex();
}

QModelIndex APIModel::parent(const QModelIndex& index) const {
  if (!index.isValid()) {
    return QModelIndex();
  }

  const auto child_item = static_cast<APIItem*>(index.internalPointer());
  const auto parent_item = child_item->parent();
  if (!parent_item.has_value()) {
    return QModelIndex();
  }

  const auto& parent_item_ref = parent_item.value().get();
  if (&parent_item_ref == root_.get()) {
    return QModelIndex();
  }
  return createIndex(parent_item_ref.row(), 0, &parent_item_ref);
}

int APIModel::rowCount(const QModelIndex& parent) const {
  APIItem::opt_ref_t parent_item;
  if (!parent.isValid()) {
    parent_item = *root_;
  } else {
    parent_item = *static_cast<APIItem*>(parent.internalPointer());
  }
  return parent_item.value().get().child_count();
}

int APIModel::columnCount(const QModelIndex& parent) const {
  return 1;
}

APISortFilterProxyModel::APISortFilterProxyModel(QObject* parent)
    : QSortFilterProxyModel(parent) {
  category_order_["C++"] = 0;
  category_order_["Rust"] = 1;
  category_order_["General"] = 2;
  category_order_["Utilities"] = 3;
  // TODO: Also sort objects within categories for a consistent view
  setSortRole(Qt::DisplayRole);
  setDynamicSortFilter(true);
}

bool APISortFilterProxyModel::lessThan(const QModelIndex& source_left,
                                       const QModelIndex& source_right) const {
  if (!source_left.parent().isValid() && !source_right.parent().isValid()) {
    const QString left_text =
        sourceModel()->data(source_left, Qt::DisplayRole).toString();
    const QString right_text =
        sourceModel()->data(source_right, Qt::DisplayRole).toString();

    const bool left_in_order = category_order_.contains(left_text);
    const bool right_in_order = category_order_.contains(right_text);

    if (left_in_order && right_in_order) {
      return category_order_[left_text] < category_order_[right_text];
    } else if (left_in_order) {
      return true;
    } else if (right_in_order) {
      return false;
    }
  }

  return QSortFilterProxyModel::lessThan(source_left, source_right);
}

}  // namespace iprm
