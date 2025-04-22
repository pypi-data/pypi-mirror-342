/*
 * Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>
 *
 * SPDX-License-Identifier: MIT
 */

#include "DependencyGraphItemFactory.hpp"
#include "DependencyGraphEdge.hpp"
#include "DependencyGraphNode.hpp"
#include "DependencyGraphicsScene.hpp"

namespace iprm {

DependencyGraphItemFactory::DependencyGraphItemFactory(QGraphicsScene* scene,
                                                       QObject* parent)
    : QObject(parent), scene_(scene) {}

void DependencyGraphItemFactory::create(const gv::LayoutResult& result) {
  clear();

  for (const auto& layout_node : result.nodes) {
    auto node = new DependencyGraphNode(layout_node);
    connect(&node->state_change_notifier(),
            &NodeStateChangeNotifier::hover_state_changed, this,
            [this](int node_id, bool hovering) {
              Q_EMIT node_hover_state_changed(nodes_[node_id], hovering);
            });
    nodes_[node->id()] = node;
    scene_->addItem(node);
  }

  for (const auto& layout_edge : result.edges) {
    auto edge =
        new DependencyGraphEdge(layout_edge, nodes_[layout_edge.source_id],
                                nodes_[layout_edge.target_id]);
    edges_.push_back(edge);
    scene_->addItem(edge);

    edge->setZValue(-1);
  }
}

void DependencyGraphItemFactory::clear() {
  for (auto& [_, node] : nodes_) {
    scene_->removeItem(node);
    delete node;
    node = nullptr;
  }
  nodes_.clear();

  for (auto& edge : edges_) {
    scene_->removeItem(edge);
    delete edge;
    edge = nullptr;
  }
  edges_.clear();
}

}  // namespace iprm
