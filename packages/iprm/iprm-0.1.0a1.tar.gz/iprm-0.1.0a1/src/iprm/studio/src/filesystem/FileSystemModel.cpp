/*
 * Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>
 *
 * SPDX-License-Identifier: MIT
 */
#include "FileSystemModel.hpp"
#include "../util/AssetCache.hpp"
#include "../util/AppTheme.hpp"
#include "../util/util.hpp"

#include <algorithm>

namespace lemon {

const Invalid INVALID = Invalid();

}  // namespace lemon

namespace iprm {

auto node_file_path(const FileNode& node) {
  return std::visit(overloaded{[](const auto& n) { return n.path; }}, node);
}

auto node_display_role(const FileNode& node) {
  return QString::fromStdString(node_file_path(node).filename().string());
}

auto node_foreground_role(const FileNode& node) {
  // TODO: These files should be a different colour, say a green-ish colour.
  //  And we should also include the `build` directory in the view that
  //  gets created on configure. That should be a reddish/orange colour.
  //  Finally, our .iprm directory for our internal project environment
  //  (right now is only a cache for .iprm file generation). Maybe that
  //  can be a blus-ish colour

  // TODO: Add colors for other special files (.iprm, build dir, etc.)

  return std::visit(
      overloaded{[](const NativeFile&) { return QVariant(); },
                 [](const Folder&) { return QVariant(); },
                 [](const auto&) {
                   return QVariant(
                       AppTheme::instance().file_foreground_colour());
                 }},
      node);
}

auto node_decoration_role(const FileNode& node) -> QIcon {
  return std::visit(
      overloaded{
          [](const auto&) { return QIcon(); },
          [](const NativeFile&) { return AssetCache::iprm_nativefile_icon(); },
          [](const BackendFile& n) { return n.backend.get().icon_; }},
      node);
}

static bool less_than(const FileNode& node_a, const FileNode& node_b) {
  const auto path_a = node_file_path(node_a);
  const auto path_b = node_file_path(node_b);
  bool is_dir_a = is_directory(path_a);
  bool is_dir_b = is_directory(path_b);
  if (is_dir_a != is_dir_b) {
    return is_dir_a > is_dir_b;
  }
  return path_a.filename().string() < path_b.filename().string();
}

FileSystemModel::FileSystemModel(QObject* parent)
    : QAbstractItemModel(parent), fs_node_data_(fs_graph_) {}

FileSystemModel::~FileSystemModel() = default;

void FileSystemModel::track_builtins(const QList<SystemBackend>& builtins) {
  for (const auto& builtin : builtins) {
    backends_.append(std::cref(builtin));
  }
}

void FileSystemModel::track_plugins(const QList<SystemBackend>& plugins) {
  for (const auto& plugin : plugins) {
    backends_.append(std::cref(plugin));
  }
}

void FileSystemModel::load_tree(const std::string& native_file_name,
                                const std::vector<std::filesystem::path>& files,
                                const std::filesystem::path& root_dir) {
  beginResetModel();
  native_file_name_ = native_file_name;
  files_ = files;
  root_dir_ = root_dir;

  fs_graph_.clear();
  sorted_children_.clear();
  parent_map_.clear();

  root_node_ = fs_graph_.addNode();
  fs_node_data_[root_node_] =
      Folder{.path = root_dir_, .parent_path = root_dir_.parent_path()};

  build_tree_structure(files_);

  for (lemon::ListDigraph::NodeIt node(fs_graph_); node != lemon::INVALID;
       ++node) {
    std::vector<lemon::ListDigraph::Node> children;
    for (lemon::ListDigraph::OutArcIt arc(fs_graph_, node);
         arc != lemon::INVALID; ++arc) {
      auto child = fs_graph_.target(arc);
      children.push_back(child);
      parent_map_[fs_graph_.id(child)] = node;
    }

    std::sort(children.begin(), children.end(),
              [this](const lemon::ListDigraph::Node& a,
                     const lemon::ListDigraph::Node& b) {
                return less_than(fs_node_data_[a], fs_node_data_[b]);
              });

    sorted_children_[fs_graph_.id(node)] = std::move(children);
  }

  endResetModel();
}

void FileSystemModel::reload_tree() {
  load_tree(native_file_name_, files_, root_dir_);
}

void FileSystemModel::build_tree_structure(
    const std::vector<std::filesystem::path>& files) {
  std::unordered_map<std::filesystem::path, lemon::ListDigraph::Node>
      path_to_node;
  path_to_node[root_dir_] = root_node_;

  // First pass: Create all directory nodes and collect IPRM files
  for (const auto& file : files) {
    if (file.filename() != native_file_name_) {
      continue;
    }

    std::filesystem::path current = file.parent_path();
    while (current != root_dir_) {
      if (path_to_node.find(current) == path_to_node.end()) {
        auto node = fs_graph_.addNode();
        path_to_node[current] = node;
        fs_node_data_[node] =
            Folder{.path = current, .parent_path = current.parent_path()};
      }
      current = current.parent_path();
    }
  }

  // Second pass: Create IPRM file nodes and check for existing generated
  // sidecars, if they exist add their nodes too
  for (const auto& native_file : files) {
    if (native_file.filename() != native_file_name_) {
      continue;
    }

    auto parent_path = native_file.parent_path();
    auto parent_node = path_to_node[parent_path];

    auto iprm_node = fs_graph_.addNode();
    fs_node_data_[iprm_node] = NativeFile{
        .path = native_file,
        .parent_path = parent_path,
    };
    fs_graph_.addArc(parent_node, iprm_node);

    for (const auto& backend : backends_) {
      const auto& file_exts = backend.get().file_exts_;
      for (const auto& file_ext : file_exts) {
        for (const auto& entry :
             std::filesystem::directory_iterator(parent_path)) {
          if (is_regular_file(entry.status())) {
            const auto entry_file_path = entry.path();
            if (entry_file_path.string().ends_with(file_ext)) {
              auto backend_node = fs_graph_.addNode();
              fs_node_data_[backend_node] = BackendFile{
                  .backend = backend.get(),
                  .native_path = native_file,
                  .path = entry_file_path,
                  .parent_path = parent_path,
              };
              fs_graph_.addArc(parent_node, backend_node);
            }
          }
        }
      }
    }
  }

  // Connect directory nodes to their parents
  for (const auto& [path, node] : path_to_node) {
    if (path == root_dir_)
      continue;

    auto parent_path = path.parent_path();
    if (auto it = path_to_node.find(parent_path); it != path_to_node.end()) {
      fs_graph_.addArc(it->second, node);
    }
  }
}

QModelIndex FileSystemModel::index(int row,
                                   int column,
                                   const QModelIndex& parent) const {
  if (!hasIndex(row, column, parent)) {
    return QModelIndex();
  }

  lemon::ListDigraph::Node parent_node;
  if (!parent.isValid()) {
    parent_node = root_node_;
  } else {
    parent_node = get_node_from_index(parent);
  }

  const auto& children = get_children(parent_node);
  if (row >= 0 && row < static_cast<int>(children.size())) {
    return create_index_from_node(row, column, children[row]);
  }

  return QModelIndex();
}

QModelIndex FileSystemModel::parent(const QModelIndex& index) const {
  if (!index.isValid()) {
    return QModelIndex();
  }

  auto node = get_node_from_index(index);
  if (node == root_node_) {
    return QModelIndex();
  }

  auto it = parent_map_.find(fs_graph_.id(node));
  if (it == parent_map_.end() || it->second == root_node_) {
    return QModelIndex();
  }

  // Find row in parent's children
  const auto& siblings = sorted_children_.at(fs_graph_.id(it->second));
  auto it_child = std::find(siblings.begin(), siblings.end(), node);
  int row = it_child != siblings.end()
                ? std::distance(siblings.begin(), it_child)
                : 0;

  return create_index_from_node(row, 0, it->second);
}

int FileSystemModel::rowCount(const QModelIndex& parent) const {
  if (parent.column() > 0) {
    return 0;
  }

  lemon::ListDigraph::Node node;
  if (!parent.isValid()) {
    node = root_node_;
  } else {
    node = get_node_from_index(parent);
  }

  return static_cast<int>(get_children(node).size());
}

int FileSystemModel::columnCount(const QModelIndex&) const {
  return 1;
}

QVariant FileSystemModel::data(const QModelIndex& index, int role) const {
  if (!index.isValid()) {
    return QVariant();
  }

  auto node = get_node_from_index(index);
  const auto& node_data = fs_node_data_[node];

  switch (role) {
    case Qt::DisplayRole:
      return node_display_role(node_data);
    case Qt::ForegroundRole:
      return node_foreground_role(node_data);
    case Qt::DecorationRole:
      return node_decoration_role(node_data);
    default:
      break;
  }

  return QVariant();
}

QVariant FileSystemModel::headerData(int section,
                                     Qt::Orientation orientation,
                                     int role) const {
  if (orientation == Qt::Horizontal && role == Qt::DisplayRole) {
    return "Project Files";
  }
  return QVariant();
}

FileNode FileSystemModel::get_file_node(const QModelIndex& index) const {
  assert(index.isValid());
  auto node = get_node_from_index(index);
  return fs_node_data_[node];
}

QModelIndex FileSystemModel::create_index_from_node(
    int row,
    int column,
    lemon::ListDigraph::Node node) const {
  return createIndex(row, column, static_cast<quintptr>(fs_graph_.id(node)));
}

lemon::ListDigraph::Node FileSystemModel::get_node_from_index(
    const QModelIndex& index) const {
  return fs_graph_.nodeFromId(static_cast<int>(index.internalId()));
}

std::vector<lemon::ListDigraph::Node> FileSystemModel::get_children(
    lemon::ListDigraph::Node node) const {
  auto it = sorted_children_.find(fs_graph_.id(node));
  return it != sorted_children_.end() ? it->second
                                      : std::vector<lemon::ListDigraph::Node>{};
}

FileSystemSortFilterProxyModel::FileSystemSortFilterProxyModel(
    FileSystemModel* source_model,
    QObject* parent)
    : QSortFilterProxyModel(parent), source_model_(source_model) {}

bool FileSystemSortFilterProxyModel::lessThan(const QModelIndex& left,
                                              const QModelIndex& right) const {
  if (source_model_ == nullptr) {
    return QSortFilterProxyModel::lessThan(left, right);
  }
  const FileNode left_node = source_model_->get_file_node(left);
  const FileNode right_node = source_model_->get_file_node(right);

  const bool is_left_folder = std::holds_alternative<Folder>(left_node);
  const bool is_right_folder = std::holds_alternative<Folder>(right_node);
  if (is_left_folder != is_right_folder) {
    return is_left_folder;
  }

  const bool is_left_native = std::holds_alternative<NativeFile>(left_node);
  const bool is_right_native = std::holds_alternative<NativeFile>(right_node);
  if (is_left_native == is_right_native) {
    return QSortFilterProxyModel::lessThan(left, right);
  }
  return is_left_native;
}

}  // namespace iprm
