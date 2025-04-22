"""
Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>

SPDX-License-Identifier: MIT
"""
import os
from pathlib import Path
from typing import Optional
from iprm.backend.backend import Backend, GenerateMode
from iprm.core.object import Object
from iprm.api.project import Project, SubDir


class ObjectGenerator:
    def __init__(self, backend: Backend):
        self._backend = backend

    def generate(self, obj: Object):
        return self._backend.generate_object(obj)


class Generator:
    def __init__(self, backend: Backend, plugin_dir: Optional[str] = None):
        self._backend = backend
        self._loader = self._backend.loader
        self._generate_mode = self._backend.generate_mode()
        self._object_generator = ObjectGenerator(self._backend)
        self._plugin_generators: list[ObjectGenerator] = []
        from iprm.util.plugins import load_generators
        internal_plugin_generators = load_generators(
            os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'plugins')))
        self._register_plugin_generators(internal_plugin_generators)
        if plugin_dir:
            external_plugin_generators = load_generators(plugin_dir)
            self._register_plugin_generators(external_plugin_generators)

    def _register_plugin_generators(self, plugin_generators):
        for plugin_name, plugin_class in plugin_generators.items():
            self._plugin_generators.append(plugin_class(self._backend))

    def generate_project(self):
        project_objects = self._loader.load_project()
        nothing_to_generate_msg = 'no files to generate' if self._generate_mode == GenerateMode.PER_FILE else 'no objects to generate'

        if project_objects is None:
            self._loader.log_sink.log_message(
                f"'{str(self._loader.platform_ctx)}' platform is not supported: {nothing_to_generate_msg}\n",
                error=True)
            return

        from itertools import chain
        num_items_to_generate = len(project_objects.keys()) if self._generate_mode == GenerateMode.PER_FILE else len(
            list(chain.from_iterable(project_objects.values()))) if project_objects is not None else 0
        if num_items_to_generate == 0:
            self._loader.log_sink.log_message(nothing_to_generate_msg)
            return

        num_items_generated = 1
        for native_file_path, objects in project_objects.items():
            def gen_log(item):
                self._loader.log_sink.log_message(
                    f"[{num_items_generated}/{num_items_to_generate}] Generating '{item}' from "
                    f"'{native_file_path}'", end='\r')

            if self._generate_mode == GenerateMode.PER_FILE:
                self._backend.is_root_item = any([isinstance(obj, Project) for obj in objects])
            self._backend.is_last_item = num_items_generated == num_items_to_generate
            self._backend.current_generated_file_header = '\n'.join(self._backend.generate_file_header())

            generate_file_name = self._backend.generate_file_name()
            if self._generate_mode == GenerateMode.PER_FILE:
                gen_log(generate_file_name)

            self._backend.current_generate_dir = Path(str(native_file_path)).parent
            generated_content = []
            if self._generate_mode == GenerateMode.PER_FILE and self._backend.add_generated_file_header():
                generated_content.append(self._backend.current_generated_file_header)

            for obj in objects:
                generate_object_name = obj.name

                if self._generate_mode == GenerateMode.PER_OBJECT:
                    self._backend.is_root_item = isinstance(obj, Project)
                    if isinstance(obj, SubDir):
                        # TODO: Currently only MSBuild uses PER_OBJECT generate mode, and it doesn't create explicit
                        #  files for a SubDir object, so for now we're just hardcoding to skip actual processing of
                        #  SubDirs
                        num_items_generated += 1
                        continue

                    generate_object_name = f'{obj.name}{self._backend.generate_file_name()}'
                    gen_log(generate_object_name)
                generated_obj_content = self._object_generator.generate(obj)
                for plugin_generator in self._plugin_generators:
                    plugin_generated_obj_content = plugin_generator.generate(obj)
                    if plugin_generated_obj_content:
                        generated_obj_content.extend(plugin_generated_obj_content)
                if not generated_obj_content:
                    continue
                if self._generate_mode == GenerateMode.PER_FILE:
                    generated_content.extend(generated_obj_content)
                elif self._generate_mode == GenerateMode.PER_OBJECT:
                    generated_content = []
                    if self._backend.add_generated_file_header():
                        generated_content.append(self._backend.current_generated_file_header)
                    generated_content.extend(generated_obj_content)
                    if self._backend.add_generated_file_footer():
                        generated_content.append(self._backend.generate_file_footer())
                    generated_file_path = self._backend.generate_file_path() / generate_object_name
                    if self._backend.generate_file_write_impl(generated_file_path, generated_content):
                        num_items_generated += 1

            if self._generate_mode == GenerateMode.PER_FILE:
                if self._backend.add_generated_file_footer():
                    generated_content.append(self._backend.generate_file_footer())
                generated_content.append('')
                generated_file_path = self._backend.generate_file_path() / generate_file_name
                if self._backend.generate_file_write_impl(generated_file_path, generated_content):
                    num_items_generated += 1

        self._loader.log_sink.log_message('')
