/*
 * Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>
 *
 * SPDX-License-Identifier: MIT
 */
#include "LoadingWidget.hpp"
#include <QVBoxLayout>

namespace iprm {

LoadingWidget::LoadingWidget(QWidget* parent) : QWidget(parent) {
  auto layout = new QVBoxLayout(this);
  layout->setAlignment(Qt::AlignCenter);

  progress_bar_ = new QProgressBar(this);
  progress_bar_->setMinimum(0);
  progress_bar_->setMaximum(0);
  progress_bar_->setTextVisible(false);
  progress_bar_->setFixedSize(150, 4);

  label_ = new QLabel(this);

  layout->addStretch(1);
  layout->addWidget(label_, 0, Qt::AlignCenter);
  layout->addWidget(progress_bar_, 0, Qt::AlignCenter);
  layout->addStretch(1);
}

void LoadingWidget::set_text(const QString& text) {
  label_->setText(text);
}

}  // namespace iprm
