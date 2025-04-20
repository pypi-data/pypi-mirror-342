/*
 * Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>
 *
 * SPDX-License-Identifier: MIT
 */
#pragma once

#include "../util/APIBridge.hpp"

#include <lemon/list_graph.h>
#include <QAbstractItemModel>
#include <QSortFilterProxyModel>

#include <filesystem>
#include <unordered_map>
#include <variant>
#include <vector>
#include <functional>

namespace iprm {

struct NativeFile {
  std::filesystem::path path;
  std::filesystem::path parent_path;
};

struct BackendFile {
  std::reference_wrapper<const SystemBackend> backend;
  std::filesystem::path native_path;
  std::filesystem::path path;
  std::filesystem::path parent_path;
};

struct Folder {
  std::filesystem::path path;
  std::filesystem::path parent_path;
};

using FileNode =
    std::variant<NativeFile, BackendFile, Folder>;

class FileSystemModel : public QAbstractItemModel {
  Q_OBJECT

 public:
  explicit FileSystemModel(QObject* parent = nullptr);
  ~FileSystemModel() override;

  void track_builtins(const QList<SystemBackend>& builtins);
  void track_plugins(const QList<SystemBackend>& plugins);

  void load_tree(const std::string& native_file_name,
                 const std::vector<std::filesystem::path>& files,
                 const std::filesystem::path& root_dir);

  void reload_tree();

  QModelIndex index(int row,
                    int column,
                    const QModelIndex& parent = QModelIndex()) const override;
  QModelIndex parent(const QModelIndex& index) const override;
  int rowCount(const QModelIndex& parent = QModelIndex()) const override;
  int columnCount(const QModelIndex& parent = QModelIndex()) const override;
  QVariant data(const QModelIndex& index,
                int role = Qt::DisplayRole) const override;
  QVariant headerData(int section,
                      Qt::Orientation orientation,
                      int role = Qt::DisplayRole) const override;

  FileNode get_file_node(const QModelIndex& index) const;

 private:
  void build_tree_structure(const std::vector<std::filesystem::path>& files);
  QModelIndex create_index_from_node(int row,
                                     int column,
                                     lemon::ListDigraph::Node node) const;
  lemon::ListDigraph::Node get_node_from_index(const QModelIndex& index) const;
  std::vector<lemon::ListDigraph::Node> get_children(
      lemon::ListDigraph::Node node) const;

  std::string native_file_name_;
  std::vector<std::filesystem::path> files_;
  std::filesystem::path root_dir_;

  QList<std::reference_wrapper<const SystemBackend>> backends_;

  lemon::ListDigraph fs_graph_;
  lemon::ListDigraph::NodeMap<FileNode> fs_node_data_;
  lemon::ListDigraph::Node root_node_;

  std::unordered_map<int, std::vector<lemon::ListDigraph::Node>>
      sorted_children_;
  std::unordered_map<int, lemon::ListDigraph::Node> parent_map_;
};

class FileSystemSortFilterProxyModel : public QSortFilterProxyModel {
  Q_OBJECT
 public:
  explicit FileSystemSortFilterProxyModel(FileSystemModel* source_model,
                                          QObject* parent = nullptr);

 protected:
  bool lessThan(const QModelIndex& left,
                const QModelIndex& right) const override;

 private:
  FileSystemModel* source_model_{nullptr};
};

}  // namespace iprm
