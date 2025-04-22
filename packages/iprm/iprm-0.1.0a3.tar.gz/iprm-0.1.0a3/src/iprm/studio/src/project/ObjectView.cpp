/*
 * Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>
 *
 * SPDX-License-Identifier: MIT
 */
#include "ObjectView.hpp"
#include "../util/AssetCache.hpp"
#include "ObjectTypeComboBox.hpp"
#include "ObjectsModel.hpp"
#include "PlatformHeaderDelegate.hpp"

#include <QDialog>
#include <QDialogButtonBox>
#include <QFormLayout>
#include <QHBoxLayout>
#include <QHeaderView>
#include <QLabel>
#include <QLineEdit>
#include <QListWidget>
#include <QListWidgetItem>
#include <QPushButton>
#include <QStackedWidget>
#include <QStandardItemModel>
#include <QTableView>

namespace iprm {

ObjectView::ObjectView(ObjectNodeEntry& object, QWidget* parent)
    : QScrollArea(parent), object_(object) {
  setWidgetResizable(true);
  setFrameShape(QFrame::Shape::NoFrame);

  platforms_ = object_.platform_objects_.keys();

  auto form_layout = new QFormLayout(this);
  form_layout->setAlignment(Qt::AlignLeft | Qt::AlignTop);
  form_layout->setContentsMargins(0, 0, 0, 0);

  form_layout->addRow(make_name_view(object.name, object.hex_colour));
  // TODO: Add project root relative directory path (will always be read only
  //  in this context)
  form_layout->addRow(make_type_view(object.type_name, object.type));
  form_layout->addRow(make_platforms_view(platforms_));

  auto platform_objects = object.platform_objects_;
  if (auto obj_props_view =
          make_properties_view(platform_objects, object.type)) {
    auto props_view = new QStackedWidget(this);
    props_view->addWidget(obj_props_view);
    connect(this, &ObjectView::type_changed, this,
            [this, props_view,
             platform_objects](const qlonglong type_flags_underlying) {
              auto type_flags = static_cast<TypeFlags>(type_flags_underlying);
              auto obj_props_view_itr =
                  object_properties_views_.find(type_flags);
              if (obj_props_view_itr != object_properties_views_.end()) {
                props_view->setCurrentWidget(obj_props_view_itr.value());
              } else {
                auto obj_props_view =
                    make_properties_view(platform_objects, type_flags);
                props_view->addWidget(obj_props_view);
                props_view->setCurrentWidget(obj_props_view);
              }
            });
    form_layout->addRow(props_view);
  }
}

QHBoxLayout* ObjectView::make_name_view(const QString& name,
                                        const QString& hex_colour) {
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
  name_layout->addWidget(new QLineEdit(name, this), 1);
  return name_layout;
}

QHBoxLayout* ObjectView::make_type_view(const QString& type_name,
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
  connect(type_combo, &ObjectTypeComboBox::type_changed, this,
          &ObjectView::type_changed);
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

QWidget* ObjectView::make_properties_view(
    const QHash<QString, QPair<QIcon, Object>>& platform_objects,
    const TypeFlags type_flags) {
  if (static_cast<bool>(type_flags & TypeFlags::SUBDIR)) {
    return nullptr;
  }

  // TODO: Add a toggle that switches between platform-specific view (column for
  //  each platform) and unified view (single column). Edits should modify the
  //  ObjectNodeEntry in real time, to allow for switching between
  //  unified/platform-specific views seamlessly as only the properties edited
  //  in unified mode will be affected, not overwriting any platform-specific
  //  things

  // TODO: On initial load, default to platform-specific view for now. This can
  //  get more sophisticated over time if need be, but lets start relatively
  //  simple

  auto props_view = new QTableView(this);
  auto props_model = new QStandardItemModel(this);
  props_model->setColumnCount(static_cast<int>(platform_objects.size()));

  QHashIterator objects_itr(platform_objects);
  int platform_column = 0;
  while (objects_itr.hasNext()) {
    objects_itr.next();
    props_model->setHeaderData(platform_column, Qt::Horizontal,
                               objects_itr.key(), Qt::DisplayRole);
    props_model->setHeaderData(platform_column, Qt::Horizontal,
                               objects_itr.value().first, Qt::DecorationRole);
    const Object& object = objects_itr.value().second;
    if (static_cast<bool>(type_flags & TypeFlags::PROJECT)) {
      // TODO: Support options property
      props_model->setRowCount(3);

      {
        static constexpr int s_version_row = 0;
        props_model->setHeaderData(s_version_row, Qt::Vertical, tr("Version"),
                                   Qt::DisplayRole);
        const QString version = object.properties["version"].toString();
        props_model->setItem(s_version_row, platform_column,
                             new QStandardItem(version));
      }
      {
        static constexpr int s_description_row = 1;
        props_model->setHeaderData(s_description_row, Qt::Vertical,
                                   tr("Description"), Qt::DisplayRole);
        const QString version = object.properties["description"].toString();
        props_model->setItem(s_description_row, platform_column,
                             new QStandardItem(version));
      }
      {
        static constexpr int s_url_row = 2;
        props_model->setHeaderData(s_url_row, Qt::Vertical, tr("URL"),
                                   Qt::DisplayRole);
        const QString version = object.properties["url"].toString();
        props_model->setItem(s_url_row, platform_column,
                             new QStandardItem(version));
      }
    }
    ++platform_column;
  }

  props_view->setModel(props_model);
  QHeaderView* header_view = props_view->horizontalHeader();
  header_view->setDefaultAlignment(Qt::AlignCenter);
  header_view->setSectionResizeMode(QHeaderView::Stretch);
  header_view->setItemDelegate(new PlatformHeaderDelegate(props_view));
  return props_view;
}

QHBoxLayout* ObjectView::make_platforms_view(const QStringList& platforms) {
  // TODO: Take in the platforms display values instead of platform.system()
  //  values
  auto platforms_layout = new QHBoxLayout();
  platforms_layout->setContentsMargins(0, 0, 0, 0);
  platforms_layout->addWidget(new QLabel(tr("Platforms:"), this), 0);
  for (const auto& platform_name : platforms) {
    auto platform_label = new QLabel(this);
    platform_label->setPixmap(AssetCache::platform_icon(platform_name)
                                  .pixmap(AssetCache::icon_size()));
    platforms_layout->addWidget(platform_label);
  }
  auto platform_select = new QPushButton("...", this);
  platform_select->setToolTip(tr("Select platforms"));
  connect(platform_select, &QPushButton::clicked, this,
          &ObjectView::on_edit_platforms);
  platforms_layout->addWidget(platform_select);
  platforms_layout->addStretch(1);
  return platforms_layout;
}

void ObjectView::on_edit_platforms() {
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
    // TODO: When platforms are removed, automatically remove/hide the platform
    //  table column for each property in the view
    // // Q_EMIT platforms_updated(selected_platforms);
  }
}

}  // namespace iprm
