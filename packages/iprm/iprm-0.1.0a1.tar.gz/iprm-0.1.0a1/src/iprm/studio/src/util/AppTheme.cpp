/*
 * Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>
 *
 * SPDX-License-Identifier: MIT
 */
#include "AppTheme.hpp"

#include "../project/TextStyle.hpp"

#if QT_VERSION >= QT_VERSION_CHECK(6, 5, 0)
#include <QStyleHints>
#include <QGuiApplication>
#else
#include <QPalette>
#include <QApplication>
#endif

namespace iprm {


AppTheme& AppTheme::instance() {
  static AppTheme instance;
  return instance;
}

AppTheme::Scheme AppTheme::os_scheme() const {
#if QT_VERSION >= QT_VERSION_CHECK(6, 5, 0)
  QStyleHints* style_hints = QGuiApplication::styleHints();
  switch (style_hints->colorScheme()) {
    case Qt::ColorScheme::Dark: {
      return Scheme::Dark;
    }
    case Qt::ColorScheme::Light:
    case Qt::ColorScheme::Unknown:
    default: {
      return Scheme::Light;
    }
  }
#else
  const bool is_dark_theme = []() {
    const QPalette palette = QApplication::palette();
    const QColor windowColor = palette.color(QPalette::Window);
    const QColor textColor = palette.color(QPalette::WindowText);
    return textColor.lightness() > windowColor.lightness();
  }();
  return is_dark_theme ? Scheme::Dark : Scheme::Light;
#endif
}

QSyntaxStyle* AppTheme::active_text_style() const {
  switch (scheme_) {
    case Scheme::Dark: {
      return TextStyle::tokyo_night();
    }
    case Scheme::Light:
    default: {
      return TextStyle::paper();
    }
  }
}

QColor AppTheme::system_colour() const {
  switch (scheme_) {
    case Scheme::Dark: {
      return Qt::white;
    }
    case Scheme::Light:
    default: {
      return Qt::black;
    }
  }
}

QColor AppTheme::file_foreground_colour() const {
  switch (scheme_) {
    case Scheme::Dark: {
      return QColor(255, 184, 108);
    }
    case Scheme::Light:
    default: {
      return QColor(139, 69, 19);
    }
  }
}

void AppTheme::update_scheme(Scheme scheme) {
  scheme_ = scheme;
  Q_EMIT scheme_changed(scheme);
}

}  // namespace iprm
