/*
 * Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>
 *
 * SPDX-License-Identifier: MIT
 */
#pragma once

#include "../../../core/src/TypeFlags.hpp"
#include "../util/APIBridge.hpp"

#include <QAbstractItemModel>
#include <QHash>
#include <QSortFilterProxyModel>
#include <QStringList>

#include <memory>

namespace iprm {

class APIItem;

class APIModel : public QAbstractItemModel {
  Q_OBJECT

 public:
  explicit APIModel(QObject* parent = nullptr);
  ~APIModel() override;

  void load(const QHash<QString, QHash<QString, APICategoryEntry>>& public_api);

  [[nodiscard]] QVariant data(const QModelIndex& index,
                              int role) const override;
  [[nodiscard]] QVariant headerData(int section,
                                    Qt::Orientation orientation,
                                    int role) const override;
  [[nodiscard]] Qt::ItemFlags flags(const QModelIndex& index) const override;

  [[nodiscard]] QModelIndex index(int row,
                                  int column,
                                  const QModelIndex& parent) const override;
  [[nodiscard]] QModelIndex parent(const QModelIndex& index) const override;

  [[nodiscard]] int rowCount(const QModelIndex& parent) const override;
  [[nodiscard]] int columnCount(const QModelIndex& parent) const override;

 private:
  std::unique_ptr<APIItem> root_;
 bool nest_third_party_extensions_{false};
};

class APISortFilterProxyModel : public QSortFilterProxyModel {
  Q_OBJECT

 public:
  explicit APISortFilterProxyModel(QObject* parent = nullptr);

 protected:
  bool lessThan(const QModelIndex& source_left,
                const QModelIndex& source_right) const override;

 private:
  QHash<QString, int> category_order_;
};

}  // namespace iprm
