/*
 * Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>
 *
 * SPDX-License-Identifier: MIT
 */
#include "LogView.hpp"

#include <QTextCursor>

namespace iprm {

LogView::LogView(const QDir& root_dir, QWidget* parent)
    : QPlainTextEdit(parent),
      root_dir_(root_dir),
      default_working_dir_(root_dir) {
  setReadOnly(true);

  // Set monospace font
  QFont font("Consolas, Monaco, monospace");
  font.setStyleHint(QFont::Monospace);
  setFont(font);

  setup_process();
}

LogView::~LogView() {
  if (process_) {
    process_->kill();
    delete process_;
  }
}

void LogView::setup_process() {
  process_ = new QProcess(this);
  process_->setWorkingDirectory(default_working_dir_.absolutePath());

  connect(process_, &QProcess::readyReadStandardOutput, this,
          &LogView::handle_stdout);
  connect(process_, &QProcess::readyReadStandardError, this,
          &LogView::handle_stderr);
  connect(process_, &QProcess::started, this,
          [this]() { Q_EMIT process_started(current_command_); });
  connect(process_, &QProcess::finished, this,
          &LogView::handle_process_finished);
  connect(process_, &QProcess::errorOccurred, this,
          [this](QProcess::ProcessError) {
            Q_EMIT process_error(process_->errorString());
          });
}

void LogView::log(const QString& text, const Type type) {
  append_to_log(text, type);
}

void LogView::log_api_error(const APIError& error) {
  log(error.message, Type::Error);
}

void LogView::start_logging_section(const QString& title) {
  append_to_log(
      QString("\n%1\n%2\n%1\n").arg(QString("=").repeated(50)).arg(title),
      Type::Section);
}

void LogView::handle_stdout() {
  QByteArray data = process_->readAllStandardOutput();
  append_to_log(QString::fromUtf8(data), Type::Normal);
}

void LogView::handle_stderr() {
  QByteArray data = process_->readAllStandardError();
  append_to_log(QString::fromUtf8(data), Type::Error);
}

void LogView::handle_process_finished(int exit_code,
                                      QProcess::ExitStatus exit_status) {
  process_->setWorkingDirectory(default_working_dir_.absolutePath());
  Q_EMIT process_finished(exit_code, exit_status);
}

void LogView::append_to_log(const QString& text, const Type type) {
  QTextCursor cursor = textCursor();
  cursor.movePosition(QTextCursor::End);

  QString processed_text = text;
  processed_text.replace("\\n", "\n");
  if (!processed_text.endsWith('\n')) {
    processed_text += '\n';
  }
  QTextCharFormat format;
  switch (type) {
    case Type::Error: {
      format.setForeground(QColor("#FF3B30"));
      break;
    }
    case Type::Section: {
      format.setForeground(QColor("#4A9EFF"));
      break;
    }
    case Type::Success: {
      format.setForeground(QColor("#34C759"));
      break;
    }
    case Type::Normal:
    default: {
      break;
    }
  }

  cursor.insertText(processed_text, format);
  setTextCursor(cursor);
}

void LogView::clear_log() {
  clear();
}

void LogView::run_command(const QString& program,
                          const QStringList& arguments,
                          const QString& working_dir) {
  current_command_ = QString("%1 %2").arg(program, arguments.join(' '));

  if (!working_dir.isEmpty()) {
    append_to_log(
        QString("Changing working directory to: %1\n").arg(working_dir),
        Type::Normal);
    process_->setWorkingDirectory(working_dir);
  }

  process_->start(program, arguments);
}

}  // namespace iprm
