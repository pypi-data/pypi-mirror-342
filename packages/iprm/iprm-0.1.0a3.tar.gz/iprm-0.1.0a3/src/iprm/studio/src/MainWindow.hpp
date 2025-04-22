/*
 * Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>
 *
 * SPDX-License-Identifier: MIT
 */
#pragma once

#include "filesystem/FileSystemModel.hpp"
#include "util/APIBridge.hpp"

#include <QDir>
#include <QDockWidget>
#include <QLabel>
#include <QMainWindow>
#include <QProcess>
#include <QProgressBar>
#include <QSettings>
#include <QStackedWidget>
#include <QStatusBar>
#include <QString>
#include <QTimer>
#include <QToolBar>
#include <QToolButton>

namespace iprm {

class FileSystemView;
class DependencyView;
class LogView;
class Project;
class APIView;
class LoadingWidget;

class MainWindow : public QMainWindow {
  Q_OBJECT

 public:
  MainWindow(APIBridgeThread& api_bridge);

  void init();

  void set_project(const QDir& project_dir);
  void load_project(const QDir& project_dir);

 public Q_SLOTS:
  void on_project_load_failed(const APIError& error) const;
  void on_project_loaded();

 private Q_SLOTS:
  void on_print_stdout(const QString& message) const;

  void on_file_activated(const FileNode& file_node) const;
  void on_file_modified(bool modified) const;
  void on_file_closed(int num_files_opened) const;

  void save_current_file();

  void new_project();
  void open_project();

  void edit_appearance();

  void show_about();

  void run_backend_generate(const QString& backend) const;

  void run_backend_configure(const QString& name,
                             const BackendConfigure& configure) const;
  void run_backend_build(const QString& name,
                         const BackendBuild& build) const;
  void run_backend_test(const QString& name,
                        const BackendTest& test) const;
  void run_backend_install(const QString& name,
                           const BackendInstall& install) const;

  void handle_process_started(const QString& command) const;
  void handle_process_finished(int exit_code, QProcess::ExitStatus exit_status);
  void handle_process_error(const QString& error_message);

 protected:
  void closeEvent(QCloseEvent* event) override;

 private:
  void create_actions();
  void create_menu_bar() const;
  void create_tool_bar();
  void setup_ui();
  void setup_api_bridge();

  APIBridgeThread& api_bridge_;

  QDir project_dir_;
  bool project_loaded_{false};
  QString file_filter_;

  QSettings settings_;

  LogView* log_view_{nullptr};
  QDockWidget* log_dock_{nullptr};

  FileSystemView* fs_view_{nullptr};
  QDockWidget* fs_dock_{nullptr};

  DependencyView* dep_view_{nullptr};
  QDockWidget* dep_dock_{nullptr};

  APIView* api_view_{nullptr};
  QDockWidget* api_dock_{nullptr};

  QStatusBar* status_bar_{nullptr};
  QLabel* status_label_{nullptr};
  QProgressBar* progress_bar_{nullptr};

  QStackedWidget* stack_{nullptr};
  Project* proj_view_{nullptr};
  QStackedWidget* proj_file_view_{nullptr};
  QWidget* no_file_view_{nullptr};

  QWidget* no_proj_view_{nullptr};
  LoadingWidget* loading_proj_view_{nullptr};
  QWidget* loading_proj_failed_view_{nullptr};

  QAction* new_action_{nullptr};
  QAction* open_action_{nullptr};
  QAction* save_action_{nullptr};

  QAction* appearance_action_{nullptr};

  QAction* about_action_{nullptr};

  // TODO: For all these actions, just make them regular tools buttons with a
  //  popup dialog, where said dialog is a QStackedWidget for each action we
  //  support. For example, the generate dialog will have a check box to say
  //  "re-generate", and configure and build, and test will allow for all the
  //  options exposed that the CLI supports, as we'll be directly invoking the
  //  IPRM CLI here now instead of building up the commands ourselves

  // TODO: add clean command for each system that removes all generated files
  //  and the binary dir (See cli testsuite for which files should be removed
  //  for each system)

  struct Backend {
    QToolButton* button_{nullptr};
    QMenu* menu_{nullptr};
    QAction* generate_action_{nullptr};
    QAction* configure_action_{nullptr};
    QAction* build_action_{nullptr};
    QAction* test_action_{nullptr};
    QAction* install_action_{nullptr};

    void enable_actions();
    void disable_actions();
  };
  QList<Backend> backends_;
};

}  // namespace iprm
