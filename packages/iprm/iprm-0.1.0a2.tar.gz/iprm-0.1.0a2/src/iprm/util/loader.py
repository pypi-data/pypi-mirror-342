"""
Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>

SPDX-License-Identifier: MIT
"""
import os
from contextlib import contextmanager
from pathlib import Path
from typing import Optional, cast
from iprm.util.platform import Platform, platform_context, PLAT_CONTEXT_TYPE, PLAT_DISPLAY_NAME
from iprm.util.meta import Meta, meta_context
from iprm.util.env import Env
from iprm.util.sink import ConsoleLogSink
from iprm.api.namespace import NAMESPACE
from iprm.core.session import Session
from iprm.core.object import Object, object_created_callback
from iprm.core.typeflags import TypeFlags
from iprm.api.project import Project, SubDir
from iprm.api.target import Target


@contextmanager
def loadable_file_context(loadable_file_path: str):
    Session.begin_file_context(loadable_file_path)
    try:
        yield
    finally:
        Session.end_file_context()


class Loader:
    def __init__(self, project_dir: str, platform: str, plugin_dir: Optional[str] = None):
        super().__init__()
        self._project_dir = project_dir
        self._platform = platform
        self._platform_ctx = PLAT_CONTEXT_TYPE[platform]()
        self._log_sink = ConsoleLogSink()
        self._backend = Meta().backend
        self._objects = {}
        self.project_object: Optional[Project] = None
        self.project_dir_abs_path: Optional[Path] = None
        self.subdir_objects: list[SubDir] = []
        self.target_objects: list[Target] = []
        self._namespace = NAMESPACE.copy()
        self._plugin_cpp_object_categories: dict[str, TypeFlags] = {}

        from iprm.util.plugins import load_objects
        internal_plugin_objects = load_objects(
            os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'plugins')))
        self._register_plugin_objects(internal_plugin_objects)

        if plugin_dir:
            external_plugin_objects = load_objects(plugin_dir)
            self._register_plugin_objects(external_plugin_objects)

    def _register_plugin_objects(self, plugin_objects):
        self._namespace.update(**plugin_objects)
        for plugin_obj_name, plugin_obj_class in plugin_objects.items():
            # TODO: Make type_flags not instance specific and expose a classmethod on Object to simplifying and
            #  generalize adding plugin objects to the categories, but for now we just hardcode to CppThirdParty
            from iprm.api.cpp import CppThirdParty
            from iprm.core.typeflags import THIRDPARTY, CPP
            if issubclass(plugin_obj_class, CppThirdParty):
                self._plugin_cpp_object_categories[plugin_obj_name] = (THIRDPARTY | CPP)

    @property
    def backend(self):
        return self._backend

    @backend.setter
    def backend(self, backend):
        self._backend = backend

    @property
    def project_dir(self):
        return self._project_dir

    @property
    def platform(self):
        return self._platform

    @property
    def platform_display(self):
        return PLAT_DISPLAY_NAME[self._platform]

    @property
    def platform_ctx(self):
        return self._platform_ctx

    @property
    def plugin_cpp_object_categories(self):
        return self._plugin_cpp_object_categories

    @property
    def log_sink(self):
        return self._log_sink

    def load_file(self, file_path):
        with loadable_file_context(file_path):
            with open(file_path, 'r') as f:
                file_contents = f.read()
                try:
                    with meta_context(self.backend, Path(file_path)):
                        Env.meta = Meta(loading=True)
                        code = compile(file_contents, file_path, 'exec')
                        self._load_code(code, self._namespace)
                except Exception as e:
                    self._log_exception(e)

    def _load_code(self, code, namespace):
        with platform_context(self._platform_ctx):
            Env.platform = Platform()
            try:
                exec(code, globals().update(**namespace))
            except Exception as e:
                self._log_exception(e)

    def _log_exception(self, e):
        import traceback
        tb_str = traceback.format_exc()
        exception_type = type(e).__name__
        error_message = str(e)
        # Access additional attributes that some exceptions might have
        extra_attrs = {attr: getattr(e, attr) for attr in dir(e)
                       if not attr.startswith('__') and not callable(getattr(e, attr))}

        self._log_sink.log_exception(e=e, type=exception_type, message=error_message, traceback=tb_str,
                                     attrs=extra_attrs)

    def load_project(self):
        loadable_project_entries = sorted([Path(native_file).absolute() for native_file in
                                           Session.retrieve_loadable_files()], key=lambda path: len(path.parts))

        num_entries_to_load = len(loadable_project_entries)
        if num_entries_to_load == 0:
            self._log_sink.log_message(f'no project files to load')
            return

        loaded_project_paths = set()
        num_entries_loaded = 1
        for entry_file_path in loadable_project_entries:

            def load_log(load):
                self._log_sink.log_message(
                    f"[{num_entries_loaded}/{num_entries_to_load}] {'Loading' if load else 'Skipping'} '{entry_file_path}'",
                    end='\r')

            entry_folder_path = entry_file_path.parent
            load_file = not loaded_project_paths or entry_folder_path in loaded_project_paths
            load_log(load_file)
            if not load_file:
                continue

            entry_file_path = str(entry_file_path)

            objects_for_file = []

            def on_objects_created(obj: Object):
                if isinstance(obj, Project):
                    if len(self._objects) != 0:
                        # TODO: Raise proper error here, Project must be the first object processed
                        pass
                    elif self.project_object is not None:
                        # TODO: Raise proper error here, there can only be a single Project object processed
                        pass
                    self.project_object = cast(Project, obj)
                    self.project_dir_abs_path = Path(self._project_dir).absolute()
                    loaded_project_paths.add(self.project_dir_abs_path)
                elif isinstance(obj, SubDir):
                    subdir = cast(SubDir, obj)
                    self.subdir_objects.append(subdir)
                    loaded_project_paths.add(subdir.path.absolute())
                elif isinstance(obj, Target):
                    self.target_objects.append(cast(Target, obj))
                objects_for_file.append(obj)

            with object_created_callback(on_objects_created):
                self.load_file(entry_file_path)

            if self.project_object is not None:
                platforms = self.project_object.properties.get('platforms', [])
                if platforms and not any([self._platform_ctx == platform for platform in platforms]):
                    # Active platform is not supported
                    return None

                # TODO: Remove this, will revisit once non-default compiler specification is actually supported
                from iprm.api.cpp import CppTarget
                from iprm.api.rust import RustTarget
                for file_obj in objects_for_file:
                    if isinstance(file_obj, CppTarget):
                        cast(CppTarget, file_obj).compiler_flag = self.project_object.cpp_compiler_flag()
                    elif isinstance(file_obj, RustTarget):
                        cast(RustTarget, file_obj).compiler_flag = self.project_object.rust_compiler_flag()

            self._objects[entry_file_path] = objects_for_file
            num_entries_loaded += 1
        self._log_sink.log_message('')
        return self._objects

    def load_project_file(self, entry_file_path):
        objects_for_file = []

        def on_objects_created(obj: Object):
            objects_for_file.append(obj)

        with object_created_callback(on_objects_created):
            self.load_file(entry_file_path)
        return objects_for_file
