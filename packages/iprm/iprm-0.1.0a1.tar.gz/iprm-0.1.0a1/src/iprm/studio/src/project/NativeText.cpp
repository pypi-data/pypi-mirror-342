/*
 * Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>
 *
 * SPDX-License-Identifier: MIT
 */
#include "NativeText.hpp"
#include "TextStyle.hpp"

#include <QGuiApplication>
#include <QMimeData>
#include <QPythonCompleter>
#include <QPythonHighlighter>
#include <QStyleHints>

namespace iprm {

NativeText::NativeText(QWidget* parent) : QCodeEditor(parent) {
  // TODO: Hook up Editor syntax style to the options page, when switching this
  //  widget should update it's styles. Should keep the full map of available
  //  styles, or have a way to ask for them
  setSyntaxStyle(TextStyle::active());
  setHighlighter(new QPythonHighlighter);
  setWordWrapMode(QTextOption::NoWrap);
  setTabReplace(true);
  setTabReplaceSize(2);
  setAcceptDrops(true);
}

void NativeText::dropEvent(QDropEvent* event) {
  const QMimeData* mimeData = event->mimeData();
  if (mimeData->hasFormat("application/x-apiitem")) {
    QByteArray encoded_data = mimeData->data("application/x-apiitem");
    QDataStream stream(&encoded_data, QIODevice::ReadOnly);

    QString name;
    int flags;
    stream >> name >> flags;

    QTextCursor cursor = textCursor();
    cursor.movePosition(QTextCursor::StartOfLine);

    const QString current_line_text = cursor.block().text().trimmed();
    if (!current_line_text.isEmpty()) {
      cursor.movePosition(QTextCursor::Up, QTextCursor::KeepAnchor);
      cursor.insertText("\n");
      cursor.movePosition(QTextCursor::Up);
    }

    // TODO: use shared unique name infra to have a better type-specific name by
    //  default and a better unique variable name by default

    // TODO: Also detect/handle types like PyBind11ThirdParty that require
    //  more in their ctor than just a name. Also handle errors gracefully on
    //  reload, as currently we crash when saving a pybind11 target added on
    //  file save
    cursor.insertText(QString("target = %0('%1')").arg(name, "new_target"));
    cursor.insertText("\n");

    event->acceptProposedAction();
  } else {
    QCodeEditor::dropEvent(event);
  }
}

}  // namespace iprm
