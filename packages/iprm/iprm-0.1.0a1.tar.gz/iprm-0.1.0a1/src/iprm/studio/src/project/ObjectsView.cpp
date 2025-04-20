/*
 * Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>
 *
 * SPDX-License-Identifier: MIT
 */
#include "ObjectsView.hpp"
#include "../util/AssetCache.hpp"
#include "ObjectsModel.hpp"

#include <QApplication>
#include <QHeaderView>
#include <QMouseEvent>
#include <QPainter>
#include <QMimeData>

namespace iprm {

ObjectsView::ObjectsView(QWidget* parent)
    : QTreeView(parent),
      model_(new ObjectsModel(this)),
      proxy_model_(new ObjectsSortFilterProxyModel(this)) {
  setHeaderHidden(false);
  setAlternatingRowColors(true);
  setSelectionMode(SingleSelection);
  setAnimated(false);
  setIndentation(0);
  setItemsExpandable(false);
  setRootIsDecorated(false);
  setSortingEnabled(true);
  setAcceptDrops(true);

  connect(this, &ObjectsView::doubleClicked, this,
          [this](const QModelIndex& index) {
            auto& object_node =
                model_->get_object_node(proxy_model_->mapToSource(index));
            Q_EMIT object_selected(object_node);
          });

  proxy_model_->setSourceModel(model_);
  setItemDelegateForColumn(0, new ObjectNameDelegate(this));
}

void ObjectsView::showEvent(QShowEvent* event) {
  header()->setStretchLastSection(false);
  header()->setSectionResizeMode(0, QHeaderView::ResizeMode::Stretch);
  header()->setSectionResizeMode(1, QHeaderView::ResizeMode::Stretch);
}

void ObjectsView::dragEnterEvent(QDragEnterEvent* event) {
  if (event->mimeData()->hasFormat("application/x-apiitem")) {
    event->acceptProposedAction();
  }
}

void ObjectsView::dragMoveEvent(QDragMoveEvent* event) {
  if (event->mimeData()->hasFormat("application/x-apiitem")) {
    event->acceptProposedAction();
  }
}

void ObjectsView::dropEvent(QDropEvent* event) {
  const QMimeData* mimeData = event->mimeData();
  if (mimeData->hasFormat("application/x-apiitem")) {
    QByteArray encoded_data = mimeData->data("application/x-apiitem");
    QDataStream stream(&encoded_data, QIODevice::ReadOnly);

    QString name;
    int flags;
    stream >> name >> flags;

    // TODO: If the index represents a group/parent item OR any item in the
    //  Utilities section, ignore the drop and cancel/fail/log a warning
    //  stating why it was ignored

    // TODO: Insert a new object node into the model with some default value
    //  (e.g. a unique name) and then automatically display it in the properties
    //  view for immediate editing
    /*
    model_->beginInsertRows(QModelIndex(), model_->rowCount(), model_->rowCount());
    ObjectNodeEntry newEntry{
      .name = name,
      .type_name = "DroppedType",  // Customize as needed
      .type = static_cast<TypeFlags>(flags),
      .hex_colour = "#FFFFFF",  // Default color, adjust as needed
      .compiler_version = "",
      .platform_objects_ = {{"DefaultPlatform", ObjectNode{name, "DroppedType", static_cast<TypeFlags>(flags)}}}
    };
    model_->objects_.append(newEntry);
    model_->endInsertRows();

    proxy_model_->sort(0, Qt::AscendingOrder);
    */
    event->acceptProposedAction();
  }
}

void ObjectsView::load(const QHash<QString, PlatformFile>& file) {
  setModel(proxy_model_);
  model_->load(file);
  proxy_model_->sort(0, Qt::AscendingOrder);
}

ObjectNameDelegate::ObjectNameDelegate(QObject* parent)
    : QStyledItemDelegate(parent) {}

void ObjectNameDelegate::paint(QPainter* painter,
                               const QStyleOptionViewItem& option,
                               const QModelIndex& index) const {
  if (!index.isValid()) {
    return;
  }

  QStyleOptionViewItem opt = option;
  initStyleOption(&opt, index);

  const QVariant name_icons_data = index.data(ObjectNameIconsRole);
  if (name_icons_data.isValid() && name_icons_data.canConvert<QList<QIcon>>()) {
    const auto icons = name_icons_data.value<QList<QIcon>>();
    if (!icons.isEmpty()) {
      painter->save();

      QStyle* style = opt.widget ? opt.widget->style() : QApplication::style();
      style->drawPrimitive(QStyle::PE_PanelItemViewItem, &opt, painter,
                           opt.widget);

      const QRect decoration_rect = style->subElementRect(
          QStyle::SE_ItemViewItemDecoration, &opt, opt.widget);
      const int icon_size = decoration_rect.height();
      const int total_icon_width =
          static_cast<int>(icons.length()) * (icon_size + 2) - 2;

      const int start_x = decoration_rect.left();
      for (int i = 0; i < icons.size(); ++i) {
        const QRect icon_rect(start_x + i * (icon_size + 2),
                              decoration_rect.top(), icon_size, icon_size);
        icons[i].paint(painter, icon_rect);
      }

      const QString text = index.data(Qt::DisplayRole).toString();
      if (!text.isEmpty()) {
        QRect text_rect = style->subElementRect(QStyle::SE_ItemViewItemText,
                                                &opt, opt.widget);

        text_rect.setLeft(start_x + total_icon_width + 4);

        int text_flags = Qt::AlignLeft | Qt::AlignVCenter;
        if (opt.features & QStyleOptionViewItem::WrapText) {
          text_flags |= Qt::TextWordWrap;
        }

        if (option.state & QStyle::State_Selected) {
          painter->setPen(opt.palette.color(QPalette::HighlightedText));
        } else {
          painter->setPen(opt.palette.color(QPalette::Text));
        }
        painter->drawText(text_rect, text_flags, text);
      }

      painter->restore();
      return;
    }
  }
  QStyledItemDelegate::paint(painter, option, index);
}

QSize ObjectNameDelegate::sizeHint(const QStyleOptionViewItem& option,
                                   const QModelIndex& index) const {
  QSize size = QStyledItemDelegate::sizeHint(option, index);

  const QVariant name_icons_data = index.data(ObjectNameIconsRole);
  if (name_icons_data.isValid() && name_icons_data.canConvert<QList<QIcon>>()) {
    const auto icons = name_icons_data.value<QList<QIcon>>();
    if (!icons.isEmpty()) {
      const int icon_size = option.decorationSize.width();
      const int num_icons = static_cast<int>(icons.length());
      const int total_icon_width =
          num_icons * icon_size + (num_icons - 1) * 2 + 4;

      const QString text = index.data(Qt::DisplayRole).toString();
      QFontMetrics fm(option.font);
      const int text_width = fm.horizontalAdvance(text);
      size.setWidth(size.width() + total_icon_width - text_width);
    }
  }

  return size;
}

}  // namespace iprm
