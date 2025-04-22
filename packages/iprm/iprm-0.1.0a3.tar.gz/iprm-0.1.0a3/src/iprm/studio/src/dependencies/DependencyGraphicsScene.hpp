/*
 * Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>
 *
 * SPDX-License-Identifier: MIT
 */
#pragma once

#include "../util/APIBridge.hpp"

#include <QGraphicsScene>

namespace iprm {
namespace gv {
struct LayoutResult;
}  // namespace gv

class DependencyGraphItemFactory;

class DependencyGraphicsScene : public QGraphicsScene {
  Q_OBJECT
 public:
  explicit DependencyGraphicsScene(QObject* parent = nullptr);

  void build_graph(const gv::LayoutResult& graph_layout);

  DependencyGraphItemFactory* item_factory() const { return item_factory_; }

 private:
  DependencyGraphItemFactory* item_factory_;
};

}  // namespace iprm
