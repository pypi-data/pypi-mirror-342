/*
 * Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>
 *
 * SPDX-License-Identifier: MIT
 */
#include "ObjectPropertiesView.hpp"
#include "../api/APIModel.hpp"
#include "../api/APIView.hpp"
#include "../util/APIBridge.hpp"
#include "../util/AssetCache.hpp"
#include "ObjectsModel.hpp"

#include <QDialog>
#include <QDialogButtonBox>
#include <QFormLayout>
#include <QGroupBox>
#include <QHBoxLayout>
#include <QLabel>
#include <QLineEdit>
#include <QListWidget>
#include <QListWidgetItem>
#include <QPushButton>
#include <QScrollArea>
#include <QStackedWidget>
#include <QTabBar>
#include <QTabWidget>
#include <QVBoxLayout>

namespace iprm {

ObjectPropertiesView::ObjectPropertiesView(QWidget* parent) : QWidget(parent) {
  auto main_layout = new QVBoxLayout(this);
  main_layout->setContentsMargins(0, 0, 0, 0);

  no_object_view_ = new QWidget(this);
  auto no_object_layout = new QVBoxLayout(no_object_view_);
  no_object_layout->setAlignment(Qt::AlignCenter);
  no_object_layout->addWidget(new QLabel(tr("Select an Object")));

  object_view_ = new QTabWidget(this);
  object_view_->setContentsMargins(0, 0, 0, 0);
  object_view_->setTabPosition(QTabWidget::North);
  object_view_->setMovable(true);
  object_view_->setTabsClosable(true);

  connect(object_view_, &QTabWidget::tabCloseRequested, this,
          &ObjectPropertiesView::on_object_tab_closed);

  view_ = new QStackedWidget(this);
  view_->addWidget(no_object_view_);
  view_->addWidget(object_view_);
  view_->setCurrentWidget(no_object_view_);

  main_layout->addWidget(view_);
}

void ObjectPropertiesView::show(ObjectNodeEntry& object) {
  // TODO: Make this a tab widget, with each object name as the tab and their
  //  hex colour icon as the icon
  auto objects_itr = object_views_.find(object.name);
  if (objects_itr != object_views_.end()) {
    object_view_->setCurrentWidget(objects_itr.value());
  } else {
    auto object_view = make_view(object);
    object_view_->addTab(
        object_view, AssetCache::colour_icon(object.hex_colour), object.name);
    object_view_->setCurrentWidget(object_view);
    object_views_[object.name] = object_view;
    object_nodes_[object.name] = &object;
  }
  view_->setCurrentWidget(object_view_);
}

void ObjectPropertiesView::on_object_tab_closed(const int tab_index) {
  const auto object_name = object_view_->tabBar()->tabText(tab_index);
  object_views_.remove(object_name);
  object_nodes_.remove(object_name);
  auto object_view = qobject_cast<QWidget*>(object_view_->widget(tab_index));
  object_view_->removeTab(tab_index);
  object_view->deleteLater();
  if (object_view_->count() == 0) {
    view_->setCurrentWidget(no_object_view_);
  }
}

QWidget* ObjectPropertiesView::make_view(ObjectNodeEntry& object) {
  auto object_view = new QScrollArea(this);
  object_view->setWidgetResizable(true);
  object_view->setFrameShape(QFrame::Shape::NoFrame);

  platforms_ = object.platform_objects_.keys();

  auto form_view = new QWidget(this);
  auto form_layout = new QFormLayout(form_view);
  form_layout->setContentsMargins(0, 0, 0, 0);

  auto general_view = new QGroupBox(tr("General"));
  auto general_layout = new QVBoxLayout(general_view);
  general_layout->setAlignment(Qt::AlignLeft | Qt::AlignTop);
  general_layout->addLayout(
      make_name_view(object.name, object.hex_colour, platforms_));
  general_layout->addLayout(make_type_view(object.type_name, object.type));
  // TODO: Add project root relative directory path (will always be read only
  //  in this context)
  form_layout->addRow(general_view);

  auto props_view = new QGroupBox(tr("Properties"));
  auto props_layout = new QVBoxLayout(props_view);
  props_layout->setAlignment(Qt::AlignLeft | Qt::AlignTop);
  // TODO: Add general properties group that is type-specific content

  // TODO: For each property, query the platform_context/compiler_flags for each
  //  method on the Object and find it's contexts. See
  //  iprm.util.platform/compiler, but there should be a
  //  'platform_context'/'compiler_flags' property for each object
  //  that has a subset of all available platforms/compilers
  form_layout->addRow(props_view);

  object_view->setWidget(form_view);
  return object_view;
}

QHBoxLayout* ObjectPropertiesView::make_name_view(
    const QString& name,
    const QString& hex_colour,
    const QStringList& platforms) {
  // TODO: When editing is supported, name changes need to update the cached
  //  object_views_ and object_nodes_ which currently point to now stale object
  //  name
  auto name_layout = new QHBoxLayout();
  name_layout->setContentsMargins(0, 0, 0, 0);
  name_layout->addWidget(new QLabel(tr("Name:"), this), 0);
  auto hex_colour_label = new QLabel(this);
  hex_colour_label->setPixmap(
      AssetCache::colour_icon(hex_colour).pixmap(AssetCache::icon_size()));
  name_layout->addWidget(hex_colour_label);
  // TODO: When the platforms change, automatically remove the platform from all
  //  other properties that no longer exists at the name level, as that MUST
  //  exist in order
  name_layout->addLayout(make_platforms_view(platforms));
  name_layout->addWidget(new QLineEdit(name, this), 1);
  return name_layout;
}

QHBoxLayout* ObjectPropertiesView::make_type_view(const QString& type_name,
                                                  TypeFlags type_flags) {
  auto type_layout = new QHBoxLayout();
  type_layout->setContentsMargins(0, 0, 0, 0);
  type_layout->addWidget(new QLabel(tr("Type:"), this), 0);
  const QString parent_text = [type_flags]() {
    if (static_cast<bool>(type_flags & TypeFlags::PROJECT) ||
        static_cast<bool>(type_flags & TypeFlags::SUBDIR)) {
      static const QString s_general("General");
      return s_general;
    }
    if (static_cast<bool>(type_flags & TypeFlags::CPP)) {
      static const QString s_cpp("C++");
      return s_cpp;
    } else if (static_cast<bool>(type_flags & TypeFlags::RUST)) {
      static const QString s_rust("Rust");
      return s_rust;
    }
    return QString{};
  }();

  auto type_combo = new ObjectTypeComboBox(this);
  auto object_type_model = type_combo->model();
  const QModelIndexList matched_parent_indices = object_type_model->match(
      object_type_model->index(0, 0, QModelIndex()), Qt::DisplayRole,
      parent_text, 1, Qt::MatchExactly);
  if (matched_parent_indices.length() == 1) {
    const QModelIndex parent_index = matched_parent_indices.first();
    const QModelIndexList matched_child_indices = object_type_model->match(
        object_type_model->index(0, 0, parent_index), Qt::DisplayRole,
        type_name, 1, Qt::MatchExactly);
    if (matched_child_indices.length() == 1) {
      const QModelIndex type_index = matched_child_indices.first();
      type_combo->setIndex(type_index);
    }
  }

  type_layout->addWidget(type_combo, 1);
  return type_layout;
}

QHBoxLayout* ObjectPropertiesView::make_platforms_view(
    const QStringList& platforms) {
  auto platforms_layout = new QHBoxLayout();
  platforms_layout->setContentsMargins(0, 0, 0, 0);
  for (const auto& platform_name : platforms) {
    auto platform_label = new QLabel(this);
    platform_label->setPixmap(AssetCache::platform_icon(platform_name)
                                  .pixmap(AssetCache::icon_size()));
    platforms_layout->addWidget(platform_label);
  }
  platforms_layout->addStretch(1);
  // TODO: Add button that opens list/selection dialog to choose from the
  //  available platforms
  auto platform_select = new QPushButton("...", this);
  platform_select->setToolTip(tr("Select platforms"));
  connect(platform_select, &QPushButton::clicked, this,
          &ObjectPropertiesView::on_edit_platforms);
  platforms_layout->addWidget(platform_select);
  return platforms_layout;
}

void ObjectPropertiesView::on_edit_platforms() {
  // TODO: Provide the object name and field context here so the platforms can
  //  be properly updated
  QDialog dialog(this);
  dialog.setWindowTitle(tr("Select Platforms"));
  dialog.setStyleSheet("");

  auto platforms_list = new QListWidget(&dialog);
  platforms_list->setSelectionMode(QListWidget::NoSelection);
  for (const auto& platform : APIBridge::supported_platform_names()) {
    auto platform_item = new QListWidgetItem(platform, platforms_list);
    platform_item->setFlags(platform_item->flags() | Qt::ItemIsUserCheckable);
    platform_item->setIcon(AssetCache::platform_icon(platform));

    // TODO: Pass in the current supported platforms for the context
    //  (object name + property) to initialize the checks
    platform_item->setCheckState(Qt::Checked);
  }
  auto button_box = new QDialogButtonBox(
      QDialogButtonBox::Ok | QDialogButtonBox::Cancel, &dialog);
  connect(button_box, &QDialogButtonBox::accepted, &dialog, &QDialog::accept);
  connect(button_box, &QDialogButtonBox::rejected, &dialog, &QDialog::reject);

  auto layout = new QVBoxLayout(&dialog);
  layout->addWidget(platforms_list);
  layout->addWidget(button_box);
  dialog.setLayout(layout);
  if (dialog.exec() == QDialog::Accepted) {
    QStringList selected_platforms;
    for (int i = 0; i < platforms_list->count(); ++i) {
      if (const QListWidgetItem* platform_item = platforms_list->item(i);
          platform_item->isSelected()) {
        selected_platforms.append(
            platform_item->data(PlatformNameRole).toString());
      }
    }

    // TODO: emit the selected platforms and the context (object name +
    //  property) they were changed for
    // Q_EMIT platforms_updated(selected_platforms);
  }
}

ObjectTypeComboBox::ObjectTypeComboBox(QWidget* parent) : QComboBox(parent) {
  auto api_model = new APIModel(this);
  api_model->load(APIBridge::public_objects_api());
  setModel(api_model);
  auto api_view = new APIView(this);
  api_view->setItemsExpandable(true);
  setView(api_view);
  api_view->expandAll();
}

void ObjectTypeComboBox::setIndex(const QModelIndex& type_index) {
  if (!type_index.isValid()) {
    return;
  }

  type_index_ = QPersistentModelIndex(type_index);

  setRootModelIndex(type_index_.parent());
  setCurrentIndex(type_index_.row());
  connect(view(), &QAbstractItemView::activated, this,
          &ObjectTypeComboBox::on_item_activated);
}

void ObjectTypeComboBox::showPopup() {
  prepare_popup();
  QComboBox::showPopup();
}

void ObjectTypeComboBox::prepare_popup() {
  if (!type_index_.isValid()) {
    return;
  }

  setRootModelIndex(QModelIndex());
  auto api_view = qobject_cast<APIView*>(view());
  api_view->expand(type_index_.parent());
  api_view->setCurrentIndex(type_index_);
}

void ObjectTypeComboBox::on_item_activated(const QModelIndex& type_index) {
  type_index_ = QPersistentModelIndex(type_index);
}

}  // namespace iprm
