/*
 * Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>
 *
 * SPDX-License-Identifier: MIT
 */
#pragma once

#include <QCodeEditor>

namespace iprm {

class NativeText : public QCodeEditor {
  Q_OBJECT

 public:
  explicit NativeText(QWidget* parent = nullptr);

 protected:
  void dropEvent(QDropEvent* event) override;
};

}  // namespace iprm
