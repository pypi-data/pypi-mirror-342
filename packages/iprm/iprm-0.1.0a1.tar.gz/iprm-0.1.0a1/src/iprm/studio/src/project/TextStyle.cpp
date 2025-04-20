/*
 * Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>
 *
 * SPDX-License-Identifier: MIT
 */
#include "TextStyle.hpp"
#include "../util/AppTheme.hpp"

#include <QFile>
#include <QGuiApplication>

namespace iprm {
namespace {

const QHash<QString, QSyntaxStyle* (*)()> g_text_styles{
    {"catppmpuccin_macciato", TextStyle::catppmpuccin_macciato},
    {"deep_ocean", TextStyle::deep_ocean},
    {"drakula", TextStyle::drakula},
    {"forest_night", TextStyle::forest_night},
    {"github_light", TextStyle::github_light},
    {"gruv_box", TextStyle::gruv_box},
    {"material_palenight", TextStyle::material_palenight},
    {"mightnight_blue", TextStyle::mightnight_blue},
    {"nord", TextStyle::nord},
    {"one_dark", TextStyle::one_dark},
    {"paper", TextStyle::paper},
    {"seashell", TextStyle::seashell},
    {"solarized_light", TextStyle::solarized_light},
    {"tokyo_night", TextStyle::tokyo_night},
    {"twilight", TextStyle::twilight}};

}

void TextStyle::load_style(QSyntaxStyle& style, const QString& fileName) {
  if (!style.isLoaded()) {
#ifdef _WIN64
    Q_INIT_RESOURCE(res);
#endif
    QFile fl(QString(":/styles/%0").arg(fileName));

    if (!fl.open(QIODevice::ReadOnly)) {
      return;
    }

    if (!style.load(fl.readAll())) {
      qDebug() << QString("Can't load style '%0'.").arg(fileName);
    }
  }
}

QSyntaxStyle* TextStyle::active() {
  return AppTheme::instance().active_text_style();
}

QSyntaxStyle* TextStyle::catppmpuccin_macciato() {
  static QSyntaxStyle style;
  load_style(style, "catppuccinmacchiato.xml");
  return &style;
}

QSyntaxStyle* TextStyle::deep_ocean() {
  static QSyntaxStyle style;
  load_style(style, "deepocean.xml");
  return &style;
}

QSyntaxStyle* TextStyle::drakula() {
  static QSyntaxStyle style;
  load_style(style, "drakula.xml");
  return &style;
}

QSyntaxStyle* TextStyle::forest_night() {
  static QSyntaxStyle style;
  load_style(style, "forestnight.xml");
  return &style;
}

QSyntaxStyle* TextStyle::github_light() {
  static QSyntaxStyle style;
  load_style(style, "githublight.xml");
  return &style;
}

QSyntaxStyle* TextStyle::gruv_box() {
  static QSyntaxStyle style;
  load_style(style, "gruvbox.xml");
  return &style;
}

QSyntaxStyle* TextStyle::material_palenight() {
  static QSyntaxStyle style;
  load_style(style, "materialpalenight.xml");
  return &style;
}

QSyntaxStyle* TextStyle::mightnight_blue() {
  static QSyntaxStyle style;
  load_style(style, "midnightblue.xml");
  return &style;
}

QSyntaxStyle* TextStyle::monokai() {
  static QSyntaxStyle style;
  load_style(style, "monokai.xml");
  return &style;
}

QSyntaxStyle* TextStyle::nord() {
  static QSyntaxStyle style;
  load_style(style, "nord.xml");
  return &style;
}

QSyntaxStyle* TextStyle::one_dark() {
  static QSyntaxStyle style;
  load_style(style, "onedark.xml");
  return &style;
}

QSyntaxStyle* TextStyle::paper() {
  static QSyntaxStyle style;
  load_style(style, "paper.xml");
  return &style;
}

QSyntaxStyle* TextStyle::seashell() {
  static QSyntaxStyle style;
  load_style(style, "seashell.xml");
  return &style;
}

QSyntaxStyle* TextStyle::solarized_light() {
  static QSyntaxStyle style;
  load_style(style, "solarizedlight.xml");
  return &style;
}

QSyntaxStyle* TextStyle::tokyo_night() {
  static QSyntaxStyle style;
  load_style(style, "tokyonight.xml");
  return &style;
}

QSyntaxStyle* TextStyle::twilight() {
  static QSyntaxStyle style;
  load_style(style, "twilight.xml");
  return &style;
}

QSyntaxStyle* TextStyle::style(const QString& style) {
  auto text_style_func_itr = g_text_styles.find(style);
  if (text_style_func_itr == g_text_styles.end()) {
    return nullptr;
  }
  return (*text_style_func_itr)();
}

const QHash<QString, QString>& TextStyle::light_theme_styles() {
  static const QHash<QString, QString> s_light_styles{
      {tr("GitHub Light"), "github_light"},
      {tr("Paper"), "paper"},
      {tr("Seashell"), "seashell"},
      {tr("Solarized Light"), "solarized_light"}};
  return s_light_styles;
}

const QHash<QString, QString>& TextStyle::dark_theme_styles() {
  static const QHash<QString, QString> s_dark_styles{
      {tr("Catppuccin Macchiato"), "catppmpuccin_macciato"},
      {tr("Deep Ocean"), "deep_ocean"},
      {tr("Dracula"), "drakula"},
      {tr("Forest Night"), "forest_night"},
      {tr("Gruvbox Dark"), "gruv_box"},
      {tr("Material Palenight"), "material_palenight"},
      {tr("Midnight Blue"), "mightnight_blue"},
      {tr("Monokai"), "monokai"},
      {tr("Nord"), "nord"},
      {tr("One Dark"), "one_dark"},
      {tr("Tokyo Night"), "tokyo_night"},
      {tr("Twilight"), "twilight"}};
  return s_dark_styles;
}

}  // namespace iprm
