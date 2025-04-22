/*
 * Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>
 *
 * SPDX-License-Identifier: MIT
 */
#include "FileSystemView.hpp"

#include <QAbstractItemModel>

namespace iprm {

FileSystemView::FileSystemView(QWidget* parent)
    : QTreeView(parent),
      fs_model_(new FileSystemModel(this)),
      fs_proxy_model_(new FileSystemSortFilterProxyModel(fs_model_, this)) {
  setHeaderHidden(true);
  setAnimated(true);
  setAlternatingRowColors(true);
  setSelectionMode(SingleSelection);
  setSelectionBehavior(SelectRows);
  connect(this, &QTreeView::activated, this, &FileSystemView::on_activated);

  fs_proxy_model_->setSourceModel(fs_model_);
}

void FileSystemView::track_builtins(const QList<SystemBackend>& builtins) {
  fs_model_->track_builtins(builtins);
}

void FileSystemView::track_plugins(const QList<SystemBackend>& plugins) {
  fs_model_->track_plugins(plugins);
}

void FileSystemView::load_tree(const std::string& native_file_name,
                               const std::vector<std::filesystem::path>& files,
                               const std::filesystem::path& root_dir) {
  setModel(fs_proxy_model_);
  fs_model_->load_tree(native_file_name, files, root_dir);
  fs_proxy_model_->sort(0, Qt::AscendingOrder);
  expandAll();
}

void FileSystemView::reload_tree() {
  fs_model_->reload_tree();
  fs_proxy_model_->sort(0, Qt::AscendingOrder);
  expandAll();
}

void FileSystemView::on_activated(const QModelIndex& index) {
  assert(fs_model_ != nullptr);
  Q_EMIT file_activated(
      fs_model_->get_file_node(fs_proxy_model_->mapToSource(index)));
}

void FileSystemView::select_file(const std::filesystem::path& file_path) {
  auto index = find_index(QModelIndex(), file_path);
  if (index.isValid()) {
    setCurrentIndex(index);
  }
}

QModelIndex FileSystemView::find_index(
    const QModelIndex& parent_index,
    const std::filesystem::path& target_path) {
  if (!model()) {
    return QModelIndex();
  }

  const int rows = model()->rowCount(parent_index);

  for (int row = 0; row < rows; ++row) {
    QModelIndex index = model()->index(row, 0, parent_index);
    const auto path = std::filesystem::path(
        model()->data(index, Qt::UserRole).toString().toStdString());

    if (path == target_path) {
      return index;
    }

    if (is_directory(path) &&
        target_path.string().find(path.string()) != std::string::npos) {
      QModelIndex child_index = find_index(index, target_path);
      if (child_index.isValid()) {
        expand(index);
        return child_index;
      }
    }
  }

  return QModelIndex();
}

}  // namespace iprm
