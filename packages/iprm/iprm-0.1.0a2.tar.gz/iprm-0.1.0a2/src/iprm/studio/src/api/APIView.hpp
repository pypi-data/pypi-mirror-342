/*
 * Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>
 *
 * SPDX-License-Identifier: MIT
 */
#pragma once

#include "../../../core/src/TypeFlags.hpp"
#include "../util/APIBridge.hpp"

#include <QTreeView>

namespace iprm {

class APIModel;
class APISortFilterProxyModel;

class APIView : public QTreeView {
  Q_OBJECT

 public:
  explicit APIView(QWidget* parent = nullptr);

  void load(const QHash<QString, QHash<QString, APICategoryEntry>>& public_api);

 protected:
  void mousePressEvent(QMouseEvent* event) override;
  void mouseMoveEvent(QMouseEvent* event) override;
  void startDrag(Qt::DropActions supportedActions);

 private:
  APIModel* model_{nullptr};
  APISortFilterProxyModel* proxy_model_{nullptr};
  QPoint drag_start_pos_;
};

}  // namespace iprm
