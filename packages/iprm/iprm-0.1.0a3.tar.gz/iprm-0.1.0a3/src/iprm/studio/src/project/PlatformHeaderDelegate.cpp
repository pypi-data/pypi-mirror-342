/*
 * Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>
 *
 * SPDX-License-Identifier: MIT
 */
#include "PlatformHeaderDelegate.hpp"

#include <QApplication>
#include <QPainter>

namespace iprm {

PlatformHeaderDelegate::PlatformHeaderDelegate(QObject* parent)
    : QStyledItemDelegate(parent) {}

void PlatformHeaderDelegate::paint(QPainter* painter,
                                   const QStyleOptionViewItem& option,
                                   const QModelIndex& index) const {
  QStyleOptionViewItem opt = option;
  initStyleOption(&opt, index);

  const QVariant icon_data = index.data(Qt::DecorationRole);
  if (icon_data.isValid() && !icon_data.isNull()) {
    painter->save();

    QStyle* style = opt.widget ? opt.widget->style() : QApplication::style();
    style->drawPrimitive(QStyle::PE_PanelItemViewItem, &opt, painter,
                         opt.widget);

    const QIcon icon = qvariant_cast<QIcon>(icon_data);
    const QString text = index.data(Qt::DisplayRole).toString();
    QFontMetrics fm(opt.font);
    const int text_width = fm.horizontalAdvance(text);
    const int total_width = icon_size_ + spacing_ + text_width;

    int x_start = opt.rect.x() + (opt.rect.width() - total_width) / 2;
    if (x_start < opt.rect.x()) {
      x_start = opt.rect.x();
    }

    const QRect icon_rect(x_start + 4,
                          opt.rect.y() + (opt.rect.height() - icon_size_) / 2,
                          icon_size_, icon_size_);
    icon.paint(painter, icon_rect);

    const QRect text_rect(icon_rect.right() + spacing_, opt.rect.y(),
                          text_width, opt.rect.height());
    if (option.state & QStyle::State_Selected) {
      painter->setPen(opt.palette.color(QPalette::HighlightedText));
    } else {
      painter->setPen(opt.palette.color(QPalette::Text));
    }
    painter->drawText(text_rect, Qt::AlignLeft | Qt::AlignVCenter, text);

    painter->restore();
    return;
  }
  QStyledItemDelegate::paint(painter, option, index);
}

QSize PlatformHeaderDelegate::sizeHint(const QStyleOptionViewItem& option,
                                       const QModelIndex& index) const {
  QSize size = QStyledItemDelegate::sizeHint(option, index);

  const QVariant icon_data = index.data(Qt::DecorationRole);
  if (icon_data.isValid() && !icon_data.isNull()) {
    const QString text = index.data(Qt::DisplayRole).toString();
    QFontMetrics fm(option.font);
    const int text_width = fm.horizontalAdvance(text);

    const int total_width = icon_size_ + spacing_ + text_width;

    size.setWidth(total_width);
    size.setHeight(qMax(size.height(), icon_size_));
  }

  return size;
}

}  // namespace iprm
