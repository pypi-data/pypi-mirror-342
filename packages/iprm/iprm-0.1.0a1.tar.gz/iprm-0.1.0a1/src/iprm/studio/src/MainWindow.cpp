/*
 * Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>
 *
 * SPDX-License-Identifier: MIT
 */
#include "MainWindow.hpp"
#include "api/APIView.hpp"
#include "dependencies/DependencyView.hpp"
#include "filesystem/FileSystemView.hpp"
#include "log/LogView.hpp"
#include "project/Project.hpp"
#include "project/TextStyle.hpp"
#include "util/AppTheme.hpp"
#include "util/AssetCache.hpp"
#include "util/LoadingWidget.hpp"
#include "util/util.hpp"

#include <QApplication>
#include <QButtonGroup>
#include <QComboBox>
#include <QDialog>
#include <QDialogButtonBox>
#include <QFileDialog>
#include <QGroupBox>
#include <QHBoxLayout>
#include <QMenuBar>
#include <QProcess>
#include <QPushButton>
#include <QRadioButton>
#include <QScrollArea>
#include <QStackedWidget>
#include <QTextEdit>
#include <QVBoxLayout>

#include <QCodeEditor>
#include <QPythonHighlighter>
#include <QStyleHints>

#include <ranges>

namespace iprm {
namespace {

const QString g_geometry_settings = "geometry";
const QString g_window_state_settings = "window_state";

}  // namespace

MainWindow::MainWindow(APIBridgeThread& api_bridge)
    : QMainWindow(nullptr),
      api_bridge_(api_bridge),
      file_filter_(tr("IPRM Project Files (build.iprm);;All Files (*.*)")),
      settings_("Intermediate Project Representation Model", "IPRM Studio") {
  setup_api_bridge();
}

void MainWindow::init() {
  connect(&api_bridge_, &APIBridgeThread::project_load_success, this,
          &MainWindow::on_project_loaded);
  setup_ui();
  create_actions();
  create_menu_bar();
  create_tool_bar();
  setWindowTitle(tr("IPRM Studio"));
  if (settings_.contains(g_geometry_settings)) {
    restoreGeometry(settings_.value(g_geometry_settings).toByteArray());
  }
  if (settings_.contains(g_window_state_settings)) {
    restoreState(settings_.value(g_window_state_settings).toByteArray());
  } else {
    static const auto s_default_window_state_settings = QByteArray::fromHex(
        "000000ff00000000fd00000002000000000000010000000206fc0200000001fb000000"
        "0e00660073005f0064006f0063006b010000003a000002060000006800ffffff000000"
        "030000078000000196fc0100000003fb00000010006100700069005f0064006f006300"
        "6b0100000000000001000000005200fffffffb00000010006c006f0067005f0064006f"
        "0063006b0100000104000003af0000005400fffffffb00000010006400650070005f00"
        "64006f0063006b01000004b7000002c90000005400ffffff0000067c00000206000000"
        "04000000040000000800000008fc0000000100000002000000010000000e0074006f00"
        "6f006c0062006100720100000000ffffffff0000000000000000");
    restoreState(s_default_window_state_settings);
  }
  resize(1280, 720);
}

void MainWindow::closeEvent(QCloseEvent* event) {
  QMainWindow::closeEvent(event);
  if (api_bridge_.isRunning()) {
    api_bridge_.destroy_sess();
    api_bridge_.quit();
    api_bridge_.wait();
  }
  settings_.setValue(g_window_state_settings, saveGeometry());
  settings_.setValue(g_window_state_settings, saveState());
}

void MainWindow::setup_api_bridge() {
  auto register_backends = [this](const QList<SystemBackend>& backends) {
    for (const auto& backend_system : backends) {
      const QString& backend_name = backend_system.name_;

      // TODO: Get icons that work with generate, configure, build ,test, and
      //  install

      // TODO: The drop down/tool menu for each represents a quick way to perform
      //  once of the supported actions for the backend. But clicking on the button
      //  directly should open up a dialog that lets you customise things more (e.g.
      //  what generator do you want to use, should be clean up and data before
      //  executing, which native or cross platform do you want to use, e.g. WASM
      //  can be executed on all platforms)

      // TODO: Allow backends to customize the tooltip for each command

      auto backend_menu = new QMenu(this);
      const auto& backend_commands = backend_system.commands_;

      QAction* generate_action = nullptr;
      QAction* configure_action = nullptr;
      QAction* build_action = nullptr;
      QAction* test_action = nullptr;
      QAction* install_action = nullptr;
      for (const auto& command : backend_commands) {
        std::visit(
            overloaded{
                [&](const BackendGenerate&) {
                  generate_action = new QAction(QIcon::fromTheme("generate"),
                                                tr("Generate"), this);
                  generate_action->setToolTip(
                      tr("Generate %0 Project").arg(backend_name));
                  connect(generate_action, &QAction::triggered, this,
                          [this, backend_name]() {
                            run_backend_generate(backend_name);
                          });
                  backend_menu->addAction(generate_action);
                },
                [&](const BackendConfigure& configure) {
                  configure_action = new QAction(QIcon::fromTheme("configure"),
                                                 tr("Configure"), this);
                  configure_action->setToolTip(
                      tr("Run %0 Configure").arg(backend_name));
                  connect(configure_action, &QAction::triggered, this,
                          [this, backend_name, configure]() {
                            run_backend_configure(backend_name, configure);
                          });
                  backend_menu->addAction(configure_action);
                },
                [&](const BackendBuild& build) {
                  build_action =
                      new QAction(QIcon::fromTheme("build"), tr("Build"), this);
                  build_action->setToolTip(
                      tr("Run %0 Build").arg(backend_name));
                  connect(build_action, &QAction::triggered, this,
                          [this, backend_name, build]() {
                            run_backend_build(backend_name, build);
                          });
                  backend_menu->addAction(build_action);
                },
                [&](const BackendTest& test) {
                  test_action =
                      new QAction(QIcon::fromTheme("test"), tr("Test"), this);
                  test_action->setToolTip(tr("Run %0 Test").arg(backend_name));
                  connect(test_action, &QAction::triggered, this,
                          [this, backend_name, test]() {
                            run_backend_test(backend_name, test);
                          });
                  backend_menu->addAction(test_action);
                },
                [&](const BackendInstall& install) {
                  install_action = new QAction(QIcon::fromTheme("install"),
                                               tr("Install"), this);
                  install_action->setToolTip(
                      tr("Run %0 Install").arg(backend_name));
                  connect(install_action, &QAction::triggered, this,
                          [this, backend_name, install]() {
                            run_backend_install(backend_name, install);
                          });
                  backend_menu->addAction(install_action);
                }},
            command);
      }

      auto backend_button = new QToolButton(this);
      backend_button->setMenu(backend_menu);
      backend_button->setPopupMode(QToolButton::MenuButtonPopup);
      backend_button->setText(backend_name);
      backend_button->setIcon(backend_system.icon_);
      backend_button->setToolButtonStyle(Qt::ToolButtonTextBesideIcon);

      backends_.emplace_back(backend_button, backend_menu, generate_action,
                             configure_action, build_action, test_action,
                             install_action);
    }
  };

  const auto& builtins = api_bridge_.builtin_backends();
  register_backends(builtins);

  const auto& plugins = api_bridge_.plugin_backends();
  register_backends(plugins);

  auto bridge = &api_bridge_;
  // TODO: Fix up error handling to not assume all returned errors are project
  //  load failures
  connect(bridge, &APIBridgeThread::error, this,
          &MainWindow::on_project_load_failed);
  connect(bridge, &APIBridgeThread::print_stdout, this,
          &MainWindow::on_print_stdout);
  api_bridge_.start();
  QMetaObject::invokeMethod(bridge, &APIBridgeThread::capture_io,
                            Qt::QueuedConnection);
}

void MainWindow::set_project(const QDir& project_dir) {
  project_dir_ = project_dir;
  if (log_view_ == nullptr) {
    log_view_ = new LogView(project_dir_, this);
  }
  QMetaObject::invokeMethod(&api_bridge_, &APIBridgeThread::load_project,
                            Qt::QueuedConnection);
}

void MainWindow::load_project(const QDir& project_dir) {
  project_dir_ = project_dir;
  project_loaded_ = false;

  // NOTE: The save actions enable state is determined by active file
  //  modification only
  new_action_->setEnabled(false);
  open_action_->setEnabled(false);
  for (auto& backend : backends_) {
    backend.disable_actions();
  }

  stack_->setCurrentWidget(loading_proj_view_);
  log_view_->start_logging_section("[Opening Project]");
  log_view_->log(QString("Loading project directory '%0'...")
                     .arg(project_dir_.absolutePath()));
  api_bridge_.set_root_dir(project_dir_);
  QMetaObject::invokeMethod(&api_bridge_, &APIBridgeThread::load_project,
                            Qt::QueuedConnection);
}

void MainWindow::setup_ui() {
  status_bar_ = statusBar();
  auto progress_widget = new QWidget(this);
  auto progress_layout = new QHBoxLayout(progress_widget);
  progress_layout->setContentsMargins(0, 0, 0, 0);
  progress_layout->setSpacing(10);

  status_label_ = new QLabel(this);
  progress_bar_ = new QProgressBar(this);
  progress_bar_->setMaximumWidth(200);
  progress_bar_->setMaximumHeight(15);
  progress_bar_->setTextVisible(false);
  progress_bar_->hide();

  progress_layout->addWidget(status_label_);
  progress_layout->addWidget(progress_bar_);
  status_bar_->addWidget(progress_widget);

  // NOTE: One may notice on Windows that resizing the dock widgets is a tiny
  // sluggish (not unusable, but definitely a 500ms or so delay from drag
  // input). Trust me, I initially thought it was my bad code too; however,
  // after looking at all my models and ensuring they aren't doing anything
  // expensive in the data() calls, and how seeing that resizing is buttery
  // smooth on my Macbook Pro with an M4 chip, we can just blame Microsoft for
  // this one. I guess a better OS and hardware always comes in clutch for us
  // application developers (jokes aside, if you know what is going on here,
  // please send in a pull request!)

  // API
  api_view_ = new APIView(this);
  api_dock_ = new QDockWidget(tr("API"));
  api_dock_->setObjectName("api_dock");
  api_dock_->setWidget(api_view_);
  addDockWidget(Qt::BottomDockWidgetArea, api_dock_);
  api_dock_->hide();

  // Log
  if (log_view_ == nullptr) {
    log_view_ = new LogView(project_dir_, this);
  }
  log_dock_ = new QDockWidget(tr("Log"));
  log_dock_->setObjectName("log_dock");
  log_dock_->setWidget(log_view_);
  addDockWidget(Qt::BottomDockWidgetArea, log_dock_);
  connect(log_view_, &LogView::process_started, this,
          &MainWindow::handle_process_started);
  connect(log_view_, &LogView::process_finished, this,
          &MainWindow::handle_process_finished);
  connect(log_view_, &LogView::process_error, this,
          &MainWindow::handle_process_error);
  log_view_->log("\nWelcome to IPRM Studio!");

  // Project
  fs_view_ = new FileSystemView(this);
  fs_view_->track_builtins(api_bridge_.builtin_backends());
  fs_view_->track_plugins(api_bridge_.plugin_backends());
  connect(fs_view_, &FileSystemView::file_activated, this,
          &MainWindow::on_file_activated);
  fs_dock_ = new QDockWidget(tr("Project"));
  fs_dock_->setObjectName("fs_dock");
  fs_dock_->setWidget(fs_view_);
  addDockWidget(Qt::LeftDockWidgetArea, fs_dock_);
  fs_dock_->hide();

  // Dependencies
  dep_view_ = new DependencyView(this);
  dep_dock_ = new QDockWidget(tr("Dependencies"));
  dep_dock_->setObjectName("dep_dock");
  dep_dock_->setWidget(dep_view_);
  addDockWidget(Qt::BottomDockWidgetArea, dep_dock_);
  dep_dock_->hide();

  // Native Project Files
  proj_file_view_ = new QStackedWidget(this);
  proj_view_ = new Project(this);
  proj_file_view_->addWidget(proj_view_);
  auto no_file_layout = new QVBoxLayout;
  no_file_layout->setAlignment(Qt::AlignCenter);
  auto no_file_label = new QLabel(tr("Select a File"), this);
  no_file_layout->addWidget(no_file_label);
  no_file_view_ = new QWidget(this);
  no_file_view_->setLayout(no_file_layout);
  connect(proj_view_, &Project::file_modified, this,
          &MainWindow::on_file_modified);
  connect(proj_view_, &Project::file_closed, this, &MainWindow::on_file_closed);
  proj_file_view_->addWidget(no_file_view_);
  proj_file_view_->setCurrentWidget(no_file_view_);

  auto no_proj_layout = new QVBoxLayout;
  no_proj_layout->setAlignment(Qt::AlignCenter);
  auto no_proj_label = new QLabel(tr("Open a Project"), this);
  no_proj_layout->addWidget(no_proj_label);
  no_proj_view_ = new QWidget(this);
  no_proj_view_->setLayout(no_proj_layout);

  auto loading_proj_failed_layout = new QHBoxLayout;
  loading_proj_failed_layout->setAlignment(Qt::AlignCenter);
  auto err_label_icon = new QLabel();
  err_label_icon->setPixmap(
      style()->standardIcon(QStyle::SP_MessageBoxCritical).pixmap(16, 16));
  auto err_label_msg =
      new QLabel(tr("Failed to load project. See Log window for more details"));
  loading_proj_failed_layout->addWidget(err_label_icon);
  loading_proj_failed_layout->addWidget(err_label_msg);
  loading_proj_failed_view_ = new QWidget(this);
  loading_proj_failed_view_->setLayout(loading_proj_failed_layout);

  loading_proj_view_ = new LoadingWidget(this);
  loading_proj_view_->set_text(tr("Loading Project..."));

  stack_ = new QStackedWidget(this);
  stack_->addWidget(no_proj_view_);
  stack_->addWidget(proj_file_view_);
  stack_->addWidget(loading_proj_failed_view_);
  stack_->addWidget(loading_proj_view_);
  stack_->setCurrentWidget(no_proj_view_);
  setCentralWidget(stack_);
}

void MainWindow::create_actions() {
  new_action_ = new QAction(QIcon::fromTheme("document-new"), tr("&New"), this);
  new_action_->setShortcut(QKeySequence::New);
  new_action_->setToolTip(tr("Create a new project"));
  connect(new_action_, &QAction::triggered, this, &MainWindow::new_project);

  open_action_ =
      new QAction(QIcon::fromTheme("document-open"), tr("&Open..."), this);
  open_action_->setShortcut(QKeySequence::Open);
  open_action_->setToolTip(tr("Open an existing project"));
  connect(open_action_, &QAction::triggered, this, &MainWindow::open_project);

  save_action_ =
      new QAction(QIcon::fromTheme("document-save"), tr("&Save"), this);
  save_action_->setShortcut(QKeySequence::Save);
  save_action_->setToolTip(tr("Save the current file"));
  connect(save_action_, &QAction::triggered, this,
          &MainWindow::save_current_file);
  save_action_->setEnabled(false);

  appearance_action_ = new QAction(tr("&Appearance..."), this);
  connect(appearance_action_, &QAction::triggered, this,
          &MainWindow::edit_appearance);

  about_action_ =
      new QAction(QIcon::fromTheme("help-about"), tr("&About..."), this);
  connect(about_action_, &QAction::triggered, this, &MainWindow::show_about);

  // TODO: Generalize this code, use a QHash<QString, GeneratorActions> where
  //  the value is the collection of all the actions the generator supports,
  //  and the key is the generator name, which we will map to the main
  //  entrypoint action


}

void MainWindow::create_menu_bar() const {
  auto file_menu = menuBar()->addMenu(tr("&File"));
  file_menu->addAction(new_action_);
  file_menu->addAction(open_action_);
  file_menu->addAction(save_action_);
  file_menu->addSeparator();

  auto settings_menu = menuBar()->addMenu(tr("&Settings"));
  settings_menu->addAction(appearance_action_);

  auto help_menu = menuBar()->addMenu(tr("&Help"));
  help_menu->addAction(about_action_);

  // TODO: Create an Options/Settings location where things like text theme for
  //  the supported file types can be set, for both dark and light mode
}

void MainWindow::create_tool_bar() {
  auto toolbar = new QToolBar(this);
  toolbar->setObjectName("toolbar");
  toolbar->setIconSize(QSize(16, 16));
  addToolBar(toolbar);

  toolbar->addAction(new_action_);
  toolbar->addAction(open_action_);
  toolbar->addAction(save_action_);

  if (!backends_.isEmpty()) {
    toolbar->addSeparator();
    for (const auto& backend : backends_) {
      toolbar->addWidget(backend.button_);
    }
  }

  toolbar->addSeparator();

  auto nexus_menu = new QMenu(this);
  // TODO: Add actions, wrapping the iprm-nexus API
  auto nexus_button = new QToolButton(this);
  nexus_button->setMenu(nexus_menu);
  nexus_button->setPopupMode(QToolButton::MenuButtonPopup);
  nexus_button->setText(tr("Nexus"));
  nexus_button->setIcon(QIcon(":/icons/nexus.svg"));
  nexus_button->setToolButtonStyle(Qt::ToolButtonTextBesideIcon);
  toolbar->addWidget(nexus_button);
  nexus_button->setToolTip(tr("IPRM Nexus is not yet available"));
}

void MainWindow::on_project_loaded() {
  fs_view_->load_tree(api_bridge_.native_file_name(), api_bridge_.file_paths(),
                      project_dir_.absolutePath().toLatin1().data());
  fs_dock_->show();

  const auto host_platform_display_name =
      api_bridge_.host_platform_display_name();
  proj_view_->set_project_dir(project_dir_);
  proj_view_->set_host_platform(host_platform_display_name,
                                AssetCache::host_platform_icon());

  dep_view_->load_graphs();
  auto platform_names = api_bridge_.platforms();
  std::ranges::sort(platform_names);
  for (const auto& platform_name : platform_names) {
    const auto& platform_display_name = api_bridge_.display(platform_name);
    const auto& platform_icon = api_bridge_.icon(platform_name);

    const auto& graph_layout =
        api_bridge_.dependency_graph_layout(platform_name);
    dep_view_->build_graph(platform_display_name, platform_icon, graph_layout);

    const auto& platform_objects = api_bridge_.objects(platform_name);
    proj_view_->add_platform(platform_display_name, platform_icon,
                             platform_objects);
  }

  dep_view_->show_graphs(host_platform_display_name);
  dep_dock_->show();

  api_view_->load(APIBridge::public_api());
  api_dock_->show();

  stack_->setCurrentWidget(proj_file_view_);

  // NOTE: The save actions enable state is determined by active file
  //  modification only
  new_action_->setEnabled(true);
  open_action_->setEnabled(true);
  for (auto& backend : backends_) {
    backend.enable_actions();
  }

  // We're ready, let it rip!
  log_view_->log(QString("\nProject directory '%0' loaded!")
                     .arg(project_dir_.absolutePath()),
                 LogView::Type::Success);
  project_loaded_ = true;
  show();
}

void MainWindow::on_project_load_failed(const APIError& error) const {
  // TODO: Setup error state, prompt user to re-try opening their folder, or
  //  opening a different one. Also ensure the log window is shown so they can
  //  see the errors that occurred during load
  log_view_->log_api_error(error);
  stack_->setCurrentWidget(loading_proj_failed_view_);
}


void MainWindow::on_print_stdout(const QString& message) const {
  log_view_->log(message);
}

void MainWindow::on_file_activated(const FileNode& file_node) const {
  proj_view_->add_file(file_node);
  proj_file_view_->setCurrentWidget(proj_view_);
}

void MainWindow::on_file_modified(const bool modified) const {
  save_action_->setEnabled(modified);
}

void MainWindow::on_file_closed(const int num_files_opened) const {
  if (num_files_opened <= 0) {
    proj_file_view_->setCurrentWidget(no_file_view_);
  }
}

void MainWindow::save_current_file() {
  FileView* current_file = proj_view_->current_file();
  const auto& file_contents = current_file->modified_file_contents();
  const auto& file_data = current_file->file_data();
  const auto& file_path = file_data.file_path;
  QFile file(file_path);
  if (!file.open(QFile::WriteOnly | QIODevice::Text)) {
    log_view_->log(tr("Unable to open file '%0' for writing").arg(file_path),
                   LogView::Type::Error);
    return;
  }
  file.write(file_contents.toUtf8());
  file.close();

  connect(
      &api_bridge_, &APIBridgeThread::project_file_load_failure, this,
      [this, current_file](const APIError& error) {
        log_view_->log_api_error(error);
        // NOTE: close the file as it is now out of sync and in a bad state,
        //  safer to just make user re-open to good back to a known/good state
        proj_view_->close_file(current_file);
      },
      Qt::SingleShotConnection);
  connect(
      &api_bridge_, &APIBridgeThread::project_file_load_success, this,
      [this, current_file,
       file_contents](const QHash<QString, PlatformFile>& platform_file) {
        current_file->update_data(file_contents, platform_file);
        dep_view_->load_graphs();
        auto platform_names = api_bridge_.platforms();
        std::ranges::sort(platform_names);
        for (const auto& platform_name : platform_names) {
          const auto& platform_display_name =
              api_bridge_.display(platform_name);
          const auto& platform_icon = api_bridge_.icon(platform_name);

          const auto& graph_layout =
              api_bridge_.dependency_graph_layout(platform_name);
          dep_view_->build_graph(platform_display_name, platform_icon,
                                 graph_layout);
        }
        const auto host_platform_display_name =
            api_bridge_.host_platform_display_name();
        dep_view_->show_graphs(host_platform_display_name);
      },
      Qt::SingleShotConnection);
  QMetaObject::invokeMethod(
      &api_bridge_,
      [this, file_path]() { api_bridge_.load_project_file(file_path); },
      Qt::QueuedConnection);
}

void MainWindow::new_project() {
  // TODO: Implement
}

void MainWindow::open_project() {
  QString dir = QFileDialog::getExistingDirectory(
      this, tr("Open IPRM Project"), QDir::homePath(),
      QFileDialog::ShowDirsOnly | QFileDialog::DontResolveSymlinks);

  if (!dir.isEmpty()) {
    load_project(QDir(dir));
  }
}

void MainWindow::edit_appearance() {
  QDialog appearance_dialog;
  appearance_dialog.setWindowTitle(tr("Appearance"));
  appearance_dialog.setMinimumWidth(550);

  auto main_layout = new QVBoxLayout(&appearance_dialog);

  auto app_theme_group = new QGroupBox(tr("Application"));
  app_theme_group->setStyleSheet(
      "QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top "
      "center; }");

  auto app_theme_layout = new QHBoxLayout(app_theme_group);

  auto light_radio = new QRadioButton(tr("Light"));
  auto dark_radio = new QRadioButton(tr("Dark"));

  auto theme_button_group = new QButtonGroup(&appearance_dialog);
  theme_button_group->addButton(light_radio);
  theme_button_group->addButton(dark_radio);

  app_theme_layout->addWidget(light_radio);
  app_theme_layout->addWidget(dark_radio);

  dark_radio->setChecked(true);

  auto editor_theme_group = new QGroupBox(tr("Code Editor"));
  editor_theme_group->setStyleSheet(
      "QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top "
      "center; }");

  auto editor_theme_layout = new QVBoxLayout(editor_theme_group);

  auto editor_theme_stacked = new QStackedWidget();

  auto light_page = new QWidget();
  auto light_layout = new QVBoxLayout(light_page);

  auto light_theme_label = new QLabel(tr("Light mode editor theme:"));
  auto light_theme_combo = new QComboBox();
  QHashIterator light_text_styles_itr(TextStyle::light_theme_styles());
  while (light_text_styles_itr.hasNext()) {
    light_text_styles_itr.next();
    light_theme_combo->addItem(light_text_styles_itr.key(),
                               light_text_styles_itr.value());
  }

  auto light_preview_edit = new QCodeEditor();
  light_preview_edit->setReadOnly(true);

  light_layout->addWidget(light_theme_label);
  light_layout->addWidget(light_theme_combo);
  light_layout->addWidget(new QLabel(tr("Preview:")));
  light_layout->addWidget(light_preview_edit);

  auto dark_page = new QWidget();
  auto dark_layout = new QVBoxLayout(dark_page);

  auto dark_theme_label = new QLabel(tr("Dark mode editor theme:"));
  auto dark_theme_combo = new QComboBox();
  QHashIterator dark_text_styles_itr(TextStyle::dark_theme_styles());
  while (dark_text_styles_itr.hasNext()) {
    dark_text_styles_itr.next();
    dark_theme_combo->addItem(dark_text_styles_itr.key(),
                              dark_text_styles_itr.value());
  }

  auto dark_preview_edit = new QCodeEditor();
  dark_preview_edit->setReadOnly(true);

  dark_layout->addWidget(dark_theme_label);
  dark_layout->addWidget(dark_theme_combo);
  dark_layout->addWidget(new QLabel(tr("Preview:")));
  dark_layout->addWidget(dark_preview_edit);

  editor_theme_stacked->addWidget(light_page);
  editor_theme_stacked->addWidget(dark_page);

  editor_theme_layout->addWidget(editor_theme_stacked);

  static const auto preview_text = QString(R"(proj = Project(
    'iprm',
    version='%0',
    description='Intermediate Project Representation Model',
)
proj.cpp()

SubDir('third_party')
SubDir('src')
)")
                                       .arg(api_bridge_.version());

  // TODO: query actual app/code editor theme currently saved

  light_preview_edit->setText(preview_text);
  light_preview_edit->setHighlighter(new QPythonHighlighter);
  light_preview_edit->setSyntaxStyle(TextStyle::paper());

  dark_preview_edit->setText(preview_text);
  dark_preview_edit->setHighlighter(new QPythonHighlighter);
  dark_preview_edit->setSyntaxStyle(TextStyle::one_dark());

  auto button_layout = new QHBoxLayout();
  button_layout->addStretch();
  auto button_box =
      new QDialogButtonBox(QDialogButtonBox::Ok | QDialogButtonBox::Cancel);
  connect(button_box, &QDialogButtonBox::accepted, &appearance_dialog,
          &QDialog::accept);
  connect(button_box, &QDialogButtonBox::rejected, &appearance_dialog,
          &QDialog::reject);
  button_layout->addWidget(button_box);

  main_layout->addWidget(app_theme_group);
  main_layout->addWidget(editor_theme_group);
  main_layout->addLayout(button_layout);

  connect(light_radio, &QRadioButton::toggled, [this, editor_theme_stacked]() {
    editor_theme_stacked->setCurrentIndex(0);
    AppTheme::instance().update_scheme(AppTheme::Scheme::Light);
  });
  connect(dark_radio, &QRadioButton::toggled, [this, editor_theme_stacked]() {
    editor_theme_stacked->setCurrentIndex(1);
    AppTheme::instance().update_scheme(AppTheme::Scheme::Dark);
  });

  auto update_editor = [](QCodeEditor* edit, const QString& style) {
    if (const auto text_style = TextStyle::style(style)) {
      edit->setSyntaxStyle(text_style);
    }
  };
  connect(
      light_theme_combo, QOverload<int>::of(&QComboBox::currentIndexChanged),
      [light_preview_edit, light_theme_combo, update_editor](const int index) {
        update_editor(light_preview_edit,
                      light_theme_combo->itemData(index).toString());
      });
  connect(
      dark_theme_combo, QOverload<int>::of(&QComboBox::currentIndexChanged),
      [dark_preview_edit, dark_theme_combo, update_editor](const int index) {
        update_editor(dark_preview_edit,
                      dark_theme_combo->itemData(index).toString());
      });

  main_layout->addStretch();

  if (appearance_dialog.exec() == QDialog::Accepted) {
    const QString app_theme = [light_radio, dark_radio]() {
      if (light_radio->isChecked()) {
        static const QString light = "Light";
        return light;
      } else if (dark_radio->isChecked()) {
        static const QString dark = "Dark";
        return dark;
      } else {
        static const QString system = "System";
        return system;
      }
    }();

    QString light_editor_theme = light_theme_combo->currentText();
    QString dark_editor_theme = dark_theme_combo->currentText();

    // TODO: Write to settings and change theme
  }
}

void MainWindow::show_about() {
  QDialog about_dialog(this);
  about_dialog.setWindowTitle(tr("About IPRM Studio"));
  about_dialog.setSizePolicy(QSizePolicy::Fixed, QSizePolicy::Fixed);
  about_dialog.setSizeGripEnabled(false);

  auto layout = new QVBoxLayout(&about_dialog);

  auto about_layout = new QHBoxLayout();
  layout->addLayout(about_layout);

  auto iprm_icon = new QLabel(&about_dialog);
  iprm_icon->setPixmap(QIcon(":/logos/iprm.svg").pixmap(128, 128));
  about_layout->addWidget(iprm_icon, 0, Qt::AlignTop | Qt::AlignLeft);

  auto iprm_info_layout = new QVBoxLayout();
  about_layout->addLayout(iprm_info_layout, 1);

  auto iprm_version = new QLabel(
      QString("IPRM Studio %0").arg(api_bridge_.version()), &about_dialog);
  QFont iprm_version_font = font();
  iprm_version_font.setPointSize(iprm_version_font.pointSize() + 6);
  iprm_version_font.setBold(true);
  iprm_version->setFont(iprm_version_font);
  iprm_info_layout->addWidget(iprm_version);

  auto iprm_license_group = new QGroupBox(tr("MIT License"));
  iprm_license_group->setStyleSheet(
      "QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top "
      "center; }");
  auto iprm_license_layout = new QVBoxLayout(iprm_license_group);

  auto iprm_license_scroll = new QScrollArea(&about_dialog);
  iprm_license_scroll->setHorizontalScrollBarPolicy(Qt::ScrollBarAlwaysOff);
  iprm_license_scroll->setVerticalScrollBarPolicy(Qt::ScrollBarAsNeeded);
  static const QString mit_text =
      R"(Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.)";
  auto iprm_license_text = new QLabel(mit_text, &about_dialog);
  iprm_license_text->setWordWrap(true);
  iprm_license_scroll->setWidgetResizable(true);
  iprm_license_scroll->setWidget(iprm_license_text);

  iprm_license_layout->addWidget(iprm_license_scroll);
  iprm_info_layout->addWidget(iprm_license_group);

  auto iprm_copyright_layout = new QHBoxLayout();
  iprm_info_layout->addLayout(iprm_copyright_layout);

  iprm_copyright_layout->addWidget(
      new QLabel("Intermediate Project Representation Model", &about_dialog));
  iprm_copyright_layout->addWidget(
      new QLabel(api_bridge_.copyright(), &about_dialog));

  auto button_layout = new QHBoxLayout();
  layout->addLayout(button_layout);
  button_layout->addStretch();
  auto button_box =
      new QDialogButtonBox(QDialogButtonBox::Close, &about_dialog);
  connect(button_box, &QDialogButtonBox::rejected, &about_dialog,
          &QDialog::reject);
  button_layout->addWidget(button_box);

  layout->addStretch();

  about_dialog.exec();
}

void MainWindow::run_backend_generate(const QString& backend) const {
  log_view_->start_logging_section(QString("[%0 Generate]").arg(backend));
  log_dock_->raise();
  QStringList args{"generate", "--backend", backend, "-p",
                         project_dir_.absolutePath()};

  const auto& plugins_dir = api_bridge_.external_plugins_dir();
  if (plugins_dir.has_value()) {
    args.append("--plugindir");
    args.append(plugins_dir.value().absolutePath());
  }

  connect(
      log_view_, &LogView::process_finished, this,
      [this, backend]() {
        log_view_->log(QString("%0 project generated for '%1'!")
                           .arg(backend, project_dir_.absolutePath()),
                       LogView::Type::Success);
        fs_view_->reload_tree();
      },
      Qt::SingleShotConnection);
  log_view_->run_command("iprm", args);
}

void MainWindow::run_backend_configure(
    const QString& name,
    const BackendConfigure& configure) const {
  log_view_->start_logging_section(QString("[%0 Configure]").arg(name));
  log_dock_->raise();
  QStringList args{"configure", "--backend", name};
  args.append(configure.args_);
  log_view_->run_command("iprm", args, project_dir_.absolutePath());
}

void MainWindow::run_backend_build(const QString& name,
                                   const BackendBuild& build) const {
  log_view_->start_logging_section(QString("[%0 Build]").arg(name));
  log_dock_->raise();
  QStringList args{"build", "--backend", name};
  args.append(build.args_);
  log_view_->run_command("iprm", args, project_dir_.absolutePath());
}
void MainWindow::run_backend_test(const QString& name,
                                  const BackendTest& test) const {
  log_view_->start_logging_section(QString("[%0 Test]").arg(name));
  log_dock_->raise();
  QStringList args{"test", "--backend", name};
  args.append(test.args_);
  log_view_->run_command("iprm", args, project_dir_.absolutePath());
}

void MainWindow::run_backend_install(
    [[maybe_unused]] const QString& name,
    [[maybe_unused]] const BackendInstall& install) const {
  QStringList args{"install", "--backend", name};
  args.append(install.args_);
  log_view_->run_command("iprm", args, project_dir_.absolutePath());
}

void MainWindow::handle_process_started(const QString& command) const {
  if (!project_loaded_) {
    return;
  }

  progress_bar_->setRange(0, 0);  // Indeterminate progress
  progress_bar_->show();
  status_label_->setText(tr("Running: %1").arg(command));
}

void MainWindow::handle_process_finished(int exit_code,
                                         QProcess::ExitStatus exit_status) {
  if (!project_loaded_) {
    return;
  }

  progress_bar_->hide();
  QTimer::singleShot(500, status_label_, &QLabel::clear);
  if (exit_code == 0 && exit_status == QProcess::NormalExit) {
    log_view_->log(tr("Command completed successfully!"),
                   LogView::Type::Success);
  } else {
    log_view_->log(tr("Command failed with exit code %0").arg(exit_code),
                   LogView::Type::Error);
  }
}

void MainWindow::handle_process_error(const QString& error_message) {
  if (!project_loaded_) {
    return;
  }

  progress_bar_->hide();
  log_view_->log(tr("Command failed: %0").arg(error_message),
                 LogView::Type::Error);
}

void MainWindow::Backend::enable_actions() {
  auto enable_action = [](QAction* action) {
    if (action != nullptr) {
      action->setEnabled(true);
    }
  };
  for (QAction* action : {generate_action_, configure_action_, build_action_,
                          test_action_, install_action_}) {
    enable_action(action);
  }
}

void MainWindow::Backend::disable_actions() {
  auto disable_action = [](QAction* action) {
    if (action != nullptr) {
      action->setDisabled(true);
    }
  };
  for (QAction* action : {generate_action_, configure_action_, build_action_,
                          test_action_, install_action_}) {
    disable_action(action);
  }
}

}  // namespace iprm
