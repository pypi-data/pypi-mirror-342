/*
 * Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>
 *
 * SPDX-License-Identifier: MIT
 */
#pragma once

#include <QColor>
#include <QObject>

class QSyntaxStyle;

namespace iprm {

class AppTheme : public QObject {
  Q_OBJECT
 public:
  enum class Scheme { Light, Dark };

  static AppTheme& instance();

  Scheme os_scheme() const;

  QSyntaxStyle* active_text_style() const;

  QColor system_colour() const;

  QColor file_foreground_colour() const;

 Q_SIGNALS:
  void scheme_changed(Scheme scheme);

 public Q_SLOTS:
  void update_scheme(Scheme scheme);

 private:
  AppTheme() = default;

  Scheme scheme_{Scheme::Light};
};

}  // namespace iprm
