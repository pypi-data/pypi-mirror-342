/*
 * Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>
 *
 * SPDX-License-Identifier: MIT
 */
#pragma once

#include <QStyledItemDelegate>

namespace iprm {

class PlatformHeaderDelegate : public QStyledItemDelegate {
 public:
  explicit PlatformHeaderDelegate(QObject* parent = nullptr);

 protected:
  void paint(QPainter* painter,
             const QStyleOptionViewItem& option,
             const QModelIndex& index) const override;

  QSize sizeHint(const QStyleOptionViewItem& option,
                 const QModelIndex& index) const override;

 private:
  static constexpr int icon_size_ = 16;
  static constexpr int spacing_ = 4;
};

}  // namespace iprm
