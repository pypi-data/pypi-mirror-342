/*
 * Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>
 *
 * SPDX-License-Identifier: MIT
 */
#include "../util/graphviz.hpp"

#include "DependencyGraphItemFactory.hpp"
#include "DependencyGraphicsScene.hpp"

namespace iprm {

DependencyGraphicsScene::DependencyGraphicsScene(QObject* parent)
    : QGraphicsScene(parent),
      item_factory_(new DependencyGraphItemFactory(this)) {
  setItemIndexMethod(NoIndex);
}

void DependencyGraphicsScene::build_graph(
    const gv::LayoutResult& graph_layout) {
  item_factory_->clear();
  clear();

  item_factory_->create(graph_layout);
}

}  // namespace iprm
