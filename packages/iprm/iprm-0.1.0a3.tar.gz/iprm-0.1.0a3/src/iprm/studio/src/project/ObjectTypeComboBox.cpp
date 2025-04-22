/*
 * Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>
 *
 * SPDX-License-Identifier: MIT
 */
#include "ObjectTypeComboBox.hpp"

#include "../api/APIItem.hpp"
#include "../api/APIModel.hpp"
#include "../api/APIView.hpp"
#include "../util/APIBridge.hpp"

namespace iprm {

ObjectTypeComboBox::ObjectTypeComboBox(QWidget* parent) : QComboBox(parent) {
  auto api_model = new APIModel(this);
  api_model->load(APIBridge::public_objects_api());
  setModel(api_model);
  auto api_view = new APIView(this);
  api_view->setItemsExpandable(true);
  setView(api_view);
  api_view->expandAll();
  connect(this, &ObjectTypeComboBox::currentIndexChanged, this,
          [this, api_model](const int index) {
            const auto type_index =
                api_model->index(index, 0, type_index_.parent());
            Q_EMIT type_changed(type_index.data(APIItemTypeRole).toLongLong());
          });
}

void ObjectTypeComboBox::setIndex(const QModelIndex& type_index) {
  if (!type_index.isValid()) {
    return;
  }

  type_index_ = QPersistentModelIndex(type_index);

  setRootModelIndex(type_index_.parent());
  setCurrentIndex(type_index_.row());
  connect(view(), &QAbstractItemView::activated, this,
          &ObjectTypeComboBox::on_item_activated);
}

void ObjectTypeComboBox::showPopup() {
  prepare_popup();
  QComboBox::showPopup();
}

void ObjectTypeComboBox::prepare_popup() {
  if (!type_index_.isValid()) {
    return;
  }

  setRootModelIndex(QModelIndex());
  auto api_view = qobject_cast<APIView*>(view());
  api_view->expand(type_index_.parent());
  api_view->setCurrentIndex(type_index_);
}

void ObjectTypeComboBox::on_item_activated(const QModelIndex& type_index) {
  type_index_ = QPersistentModelIndex(type_index);
}

}  // namespace iprm
