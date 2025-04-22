/*
 * Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>
 *
 * SPDX-License-Identifier: MIT
 */
#pragma once

#include <QComboBox>

namespace iprm {

class ObjectTypeComboBox : public QComboBox {
  Q_OBJECT
 public:
  explicit ObjectTypeComboBox(QWidget* parent = nullptr);

  void setIndex(const QModelIndex& type_index);

 Q_SIGNALS:
  void index_changed(const QModelIndex& type_index);
  void type_changed(qlonglong type_flags_underlying);

 protected:
  void showPopup() override;

 private Q_SLOTS:
  void prepare_popup();

  void on_item_activated(const QModelIndex& type_index);

 private:
  QPersistentModelIndex type_index_;
};


}  // namespace iprm
