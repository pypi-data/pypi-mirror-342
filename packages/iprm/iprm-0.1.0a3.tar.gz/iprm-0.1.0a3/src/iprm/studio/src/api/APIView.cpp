/*
 * Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>
 *
 * SPDX-License-Identifier: MIT
 */
#include "APIView.hpp"
#include "../util/AssetCache.hpp"
#include "APIModel.hpp"

#include <QApplication>
#include <QDrag>
#include <QMimeData>
#include <QMouseEvent>

namespace iprm {

APIView::APIView(QWidget* parent)
    : QTreeView(parent),
      model_(new APIModel(this)),
      proxy_model_(new APISortFilterProxyModel(this)) {
  setHeaderHidden(true);
  setAnimated(true);
  setAlternatingRowColors(true);
  setSelectionMode(SingleSelection);
  setSelectionBehavior(SelectRows);
  setDragEnabled(true);
  setAcceptDrops(false);

  proxy_model_->setSourceModel(model_);
  connect(model_, &QAbstractItemModel::modelReset, this, &QTreeView::expandAll);
  // TODO: When Project Files are editable, add ability to add a type, being
  //  prompted for the platforms
}

void APIView::load(
    const QHash<QString, QHash<QString, APICategoryEntry>>& public_api) {
  setModel(proxy_model_);
  model_->load(public_api);
  proxy_model_->sort(0, Qt::AscendingOrder);
  expandAll();
}

void APIView::mousePressEvent(QMouseEvent* event) {
  if (event->button() == Qt::LeftButton) {
    drag_start_pos_ = event->pos();
  }
  QTreeView::mousePressEvent(event);
}

void APIView::mouseMoveEvent(QMouseEvent* event) {
  if (!(event->buttons() & Qt::LeftButton)) {
    return;
  }

  if ((event->pos() - drag_start_pos_).manhattanLength() <
      QApplication::startDragDistance()) {
    return;
  }

  QModelIndex index = indexAt(drag_start_pos_);
  if (index.isValid()) {
    startDrag(Qt::MoveAction | Qt::CopyAction);
  }
}

void APIView::startDrag(Qt::DropActions supportedActions) {
  QModelIndex index =  proxy_model_->mapToSource(currentIndex());
  if (!index.isValid()) {
    return;
  }

  // TODO: If the index represents a group/parent item, don't accept the drag
  //  start and mark it as invalid so it can't even be dropped

  auto mime_data = new QMimeData;
  const QVariant data = model_->data(index, Qt::DisplayRole);
  const QString name = data.toString();
  mime_data->setText(name);
  QByteArray encoded_data;
  QDataStream stream(&encoded_data, QIODevice::WriteOnly);
  stream << name;
  // TODO: Include all the fields required in ObjectNodeEntry associated with
  //  this object, each APIItem should define all these so we can simply query them.
  /*
  * QVariant flagsData = model_->data(index, APIItem::FlagsRole);
  int flags = flagsData.toInt();
  stream << flags;
   */

  mime_data->setData("application/x-apiitem", encoded_data);

  auto drag = new QDrag(this);
  drag->setMimeData(mime_data);

  const QVariant icon_data = model_->data(index, Qt::DecorationRole);
  if (icon_data.canConvert<QIcon>()) {
    const QIcon icon = qvariant_cast<QIcon>(icon_data);
    drag->setPixmap(icon.pixmap(AssetCache::icon_size()));
  }

  drag->exec(supportedActions);
}

}  // namespace iprm
