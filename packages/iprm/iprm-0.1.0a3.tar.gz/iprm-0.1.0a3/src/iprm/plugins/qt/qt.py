"""
Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>

SPDX-License-Identifier: MIT
"""
from pathlib import Path
from typing import cast, Optional
from iprm.util.env import Env
from iprm.util.platform import platform_context
from iprm.backend.backend import Backend
from iprm.backend.cmake import CMake
from iprm.backend.meson import Meson
from iprm.generator.generator import ObjectGenerator
from iprm.core.object import Object
from iprm.core.session import Session
from iprm.api.cpp import CppTarget, CppThirdParty
from iprm.api.builder import PrecompiledArchiveBuilder
from iprm.util.dir import Dir
from iprm.core.typeflags import ARCHIVE, PRECOMPILED


class QtPrecompiledArchiveBuilder(PrecompiledArchiveBuilder):
    def __init__(self, third_party_target, archive_dir: Dir, archive_file: str):
        super().__init__(third_party_target, archive_dir, archive_file)
        self._modules: list[str] = []
        self._lib_type: str = ''

    def shared_lib_pattern(self, **kwargs):
        super()._lib_pattern(**kwargs)
        self._lib_type = 'shared'

    def static_lib_pattern(self, **kwargs):
        super()._lib_pattern(**kwargs)
        self._lib_type = 'static'

    # TODO: Add ability to customize the actual module name for each Qt core in case of custom Qt build that deviates
    #  from Qts naming conventions here

    def core(self):
        self._module('Core')

    def network(self):
        self._module('Network')

    def networkauth(self):
        self._module('NetworkAuth')

    def gui(self):
        self._module('Gui')

    def widgets(self):
        self._module('Widgets')

    def svg(self):
        self._module('Svg')

    # TODO: Add remaining modules when needed

    def _module(self, name):
        if self._lib_type == 'shared':
            self._shared_pattern_libraries.append(name)
        elif self._lib_type == 'static':
            self._static_pattern_libraries.append(name)

    def tools(self, **kwargs):
        if kwargs.get('moc', False):
            self._auxiliary_apps.append(f'moc{self.app_suffix()}')
        if kwargs.get('rcc', False):
            self._auxiliary_apps.append(f'rcc{self.app_suffix()}')
        if kwargs.get('uic', False):
            self._auxiliary_apps.append(f'uic{self.app_suffix()}')

    def build(self):
        targets = super().build()
        for target in targets:
            target.hex_colour = self._target.hex_colour
        self._target.properties['bin_dir'] = self._bin_dir
        return targets


class QtThirdParty(CppThirdParty):
    MOC = 'moc'
    RCC = 'rcc'
    UIC = 'uic'
    CONF = 'conf'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hex_colour = '#41CD52'

    @classmethod
    def svg_icon_path(cls):
        # https://upload.wikimedia.org/wikipedia/commons/0/0b/Qt_logo_2016.svg
        return Path(__file__).parent / 'qt.svg'

    def homebrew(self, **kwargs):
        imported_targets = super().homebrew(**kwargs)
        for target in imported_targets:
            target.hex_colour = self.hex_colour
        return imported_targets

    def pkgconfig(self, **kwargs):
        imported_targets = super().pkgconfig(**kwargs)
        for target in imported_targets:
            target.hex_colour = self.hex_colour
        return imported_targets

    def precompiled_archive(self, archive_dir: Dir, archive_file: str):
        self.type_flags |= (ARCHIVE | PRECOMPILED)
        return QtPrecompiledArchiveBuilder(self, archive_dir, archive_file)

    def moc(self):
        self.properties[QtThirdParty.MOC] = True

    def rcc(self):
        self.properties[QtThirdParty.RCC] = True

    def uic(self):
        self.properties[QtThirdParty.UIC] = True

    def conf(self):
        self.properties[QtThirdParty.CONF] = True


class QtObjectGenerator(ObjectGenerator):
    def __init__(self, backend: Backend):
        super().__init__(backend)

    @staticmethod
    def _requires_qt(cpp: CppTarget) -> Optional[QtThirdParty]:
        dependencies = cpp.dependencies
        with platform_context(Env.platform):
            for dependency in dependencies:
                dependency_obj = Session.get_object(dependency)
                if isinstance(dependency_obj, QtThirdParty):
                    # NOTE: Assuming targets only depend on a single qt library. If there ever is a project that
                    # requires more than one, that is a problem for future IPRM
                    return dependency_obj
        return None

    def generate(self, obj: Object):
        if not obj.is_cpp:
            return []
        cpp = cast(CppTarget, obj)
        qt_third = QtObjectGenerator._requires_qt(cpp)
        if not cpp.is_third_party and qt_third:
            if isinstance(self._backend, CMake):
                return self._generate_cmake_qt_first_party(cpp, qt_third)
            elif isinstance(self._backend, Meson):
                return self._generate_meson_qt_first_party(cpp, qt_third)
        elif isinstance(cpp, QtThirdParty) or QtObjectGenerator._requires_qt(cpp):
            cpp_third = cast(CppThirdParty, cpp)
            if isinstance(self._backend, CMake):
                return self._generate_cmake_qt_third_party(cpp_third, qt_third)
            elif isinstance(self._backend, Meson):
                return self._generate_meson_qt_first_party(cpp_third, qt_third)
        return []

    @staticmethod
    def _cmake_qt_utils_module_file():
        return CMake.cmake_modules_dir / 'qt_utils.cmake'

    def _generate_cmake_qt_first_party(self, cpp: CppTarget, qt_third: QtThirdParty):
        return self._generate_cmake_qt_sources(cpp, qt_third)

    def _generate_cmake_qt_third_party(self, cpp_third: CppThirdParty, qt_third: Optional[QtThirdParty]):
        # TODO: Support other types of third party libraries depending on Qt
        if qt_third and cpp_third.is_source_archive:
            return self._generate_cmake_qt_sources(cpp_third, qt_third,
                                                   target=cpp_third.properties.get('build_target', None))
        cpp_qt_third = cast(QtThirdParty, cpp_third)
        if cpp_third.is_precompiled_archive:
            return self._generate_cmake_qt_precompiled_archive(cpp_qt_third)
        elif cpp_third.is_pkgconfig:
            return self._generate_cmake_qt_pkgconfig(cpp_qt_third)
        elif cpp_third.is_homebrew:
            return self._generate_cmake_qt_homebrew(cpp_qt_third)
        return []

    def _generate_cmake_qt_sources(self, cpp: CppTarget, qt_third: QtThirdParty, target=None):
        cmake_content = []
        target = target if target else cpp.name

        cmake_backend = cast(CMake, self._backend)

        cmake_content.append('include(qt_utils)')
        if qt_third.properties.get(QtThirdParty.MOC, False):
            if cpp.is_source_archive:
                unpack_target_name = cpp.properties.get('unpack_target_name')
                cmake_content.append(f'iprm_qt_automoc_source_archive({target} {unpack_target_name})')
            else:
                cmake_content.append(f'iprm_qt_automoc({target})')
        if qt_third.properties.get(QtThirdParty.RCC, False):
            cmake_content.append(f'iprm_qt_autorcc({target})')
        if qt_third.properties.get(QtThirdParty.UIC, False):
            cmake_content.append(f'iprm_qt_autouic({target})')
        if (cpp.is_app or cpp.is_test) and qt_third.properties.get(QtThirdParty.CONF, False):
            qt_conf_content = """[Paths]
Prefix=@IPRM_QT_ROOT_DIR@
Plugins=@IPRM_QT_ROOT_DIR@/plugins
"""
            qt_conf_template_file = cmake_backend.current_generate_dir / 'qt.conf.in'
            qt_conf_template_file.write_text(qt_conf_content)
            output_dir = cpp.properties.get('output_dir', None)
            if output_dir:
                cmake_content.append(
                    f'configure_file("${{CMAKE_CURRENT_SOURCE_DIR}}/qt.conf.in" {cmake_backend.relative_src_path(output_dir, "qt.conf")} @ONLY)')
            else:
                cmake_content.append(
                    'configure_file("${CMAKE_CURRENT_SOURCE_DIR}/qt.conf.in" "${CMAKE_CURRENT_BINARY_DIR}/qt.conf" @ONLY)')
        if not Env.platform.windows:
            # TODO: Generalize this RPATH infrastructure in the first_party section
            cmake_content.extend([
                f'set_target_properties({target}',
                '\tPROPERTIES',
            ])
            cmake_content.append(f'\t\tBUILD_RPATH "${{IPRM_QT_ROOT_DIR}}/lib"')
            if Env.platform.macos:
                cmake_content.append(f'\t\tMACOSX_RPATH ON')
            cmake_content.append(')')
        return cmake_content

    def _generate_cmake_qt_precompiled_archive(self, cpp_third: QtThirdParty):
        cmake_content = []
        unpack_target_name = cpp_third.properties.get('unpack_target_name')
        exe_suffix = ".exe" if Env.platform.windows else ""
        # TODO: Merge the source_archive moc helper into the main automoc helper, but initially this was the only
        #  way I could get the source archive workflow working initially and didn't want to bother merging the two
        #  immediately. If ain't broke...
        if not self._cmake_qt_utils_module_file().parent.exists():
            self._cmake_qt_utils_module_file().parent.mkdir(parents=True)
        self._cmake_qt_utils_module_file().write_text(f"""{self._backend.current_generated_file_header}
set(IPRM_QT_ROOT_DIR "${{CMAKE_BINARY_DIR}}/{cpp_third.root_relative_dir.path.as_posix()}" CACHE PATH "Root Qt Directory")
set(IPRM_QT_BIN_DIR "${{IPRM_QT_ROOT_DIR}}/{cpp_third.properties.get('bin_dir').path.as_posix()}" CACHE PATH "Root Qt Binary Directory")
set(IPRM_QT_MOC_EXECUTABLE "${{IPRM_QT_BIN_DIR}}/moc{exe_suffix}" CACHE PATH "Qt MOC Executable")
set(IPRM_QT_RCC_EXECUTABLE "${{IPRM_QT_BIN_DIR}}/rcc{exe_suffix}" CACHE PATH "Qt RCC Executable")
set(IPRM_QT_UIC_EXECUTABLE "${{IPRM_QT_BIN_DIR}}/uic{exe_suffix}" CACHE PATH "Qt UIC Executable")
set(IPRM_QT_UNPACK_TARGET_NAME {unpack_target_name} CACHE STRING "Qt Unpack Precompiled Archive Target Name")

{self._cmake_qt_automoc()}

# Source archive specific automoc helper fixing issue with CMake having to generate its target build system file(s) 
# twice, at least with Ninja, for the headers to actually get MOC'd
function(iprm_qt_automoc_source_archive target unpack_target)
    get_target_property(target_sources ${{target}} SOURCES)
    foreach(source ${{target_sources}})
        if(source MATCHES "\\.(h|hpp)$")
            get_filename_component(directory ${{source}} DIRECTORY)
            get_filename_component(filename ${{source}} NAME_WE)
            get_filename_component(ext ${{source}} EXT)
            set(moc_input "${{directory}}/${{filename}}${{ext}}")
            file(RELATIVE_PATH rel_directory ${{CMAKE_CURRENT_SOURCE_DIR}} ${{directory}})
            set(moc_output "${{CMAKE_CURRENT_BINARY_DIR}}/${{rel_directory}}/moc_${{filename}}.cpp")
            set(moc_includes "$<LIST:TRANSFORM,$<TARGET_PROPERTY:third_k_editor_objects,INTERFACE_INCLUDE_DIRECTORIES>,PREPEND,-I>")

            file(RELATIVE_PATH rel_moc_input "${{CMAKE_SOURCE_DIR}}" "${{moc_input}}")

            add_custom_command(
                    OUTPUT ${{moc_output}}
                    COMMAND ${{IPRM_QT_MOC_EXECUTABLE}}
                    ${{moc_includes}}
                    ${{moc_input}}
                    -o ${{moc_output}}
                    DEPENDS
                    ${{source}} ${{IPRM_QT_UNPACK_TARGET_NAME}} ${{unpack_target}}
                    COMMENT "MOC ${{rel_moc_input}}"
                    VERBATIM
                    COMMAND_EXPAND_LISTS
            )
            target_sources(${{target}} PRIVATE ${{moc_output}})
        endif()
    endforeach()
endfunction()

{self._cmake_qt_autorcc()}

{self._cmake_qt_autouic()}
""")
        return cmake_content

    def _generate_cmake_qt_homebrew(self, cpp_third: QtThirdParty):
        cmake_content = []
        if not self._cmake_qt_utils_module_file().parent.exists():
            self._cmake_qt_utils_module_file().parent.mkdir(parents=True)
        # TODO: Maybe use python pkg-config library instead so each target that includes the
        #   qt utils doesn't need to invoke the process, that way we can just hardcode the
        #   module file. That being said, it is cheap/quick, so this is fine for now
        self._cmake_qt_utils_module_file().write_text(f"""{self._backend.current_generated_file_header}
execute_process(
	COMMAND brew --prefix
	OUTPUT_VARIABLE BREW_PREFIX
	OUTPUT_STRIP_TRAILING_WHITESPACE
)
set(QT6_QMAKE_BIN "${{BREW_PREFIX}}/bin/qmake")                  
execute_process(
    COMMAND ${{QT6_QMAKE_BIN}} -query QT_INSTALL_DATA
    OUTPUT_VARIABLE HOMEBREW_QT_ROOT_DIR
    OUTPUT_STRIP_TRAILING_WHITESPACE
)
execute_process(
  COMMAND ${{QT6_QMAKE_BIN}} -query QT_INSTALL_LIBEXECS
  OUTPUT_VARIABLE QT6_LIBEXECDIR
  OUTPUT_STRIP_TRAILING_WHITESPACE
)
set(IPRM_QT_ROOT_DIR "${{HOMEBREW_QT_ROOT_DIR}}" CACHE PATH "Root Qt Directory")
set(IPRM_QT_MOC_EXECUTABLE "${{QT6_LIBEXECDIR}}/moc" CACHE PATH "Qt MOC Executable")
set(IPRM_QT_RCC_EXECUTABLE "${{QT6_LIBEXECDIR}}/rcc" CACHE PATH "Qt RCC Executable")
set(IPRM_QT_UIC_EXECUTABLE "${{QT6_LIBEXECDIR}}/uic" CACHE PATH "Qt UIC Executable")

{self._cmake_qt_automoc()}

# Source archive specific automoc helper fixing issue with CMake having to generate its target build system file(s) 
# twice, at least with Ninja, for the headers to actually get MOC'd
function(iprm_qt_automoc_source_archive target unpack_target)
	get_target_property(target_sources ${{target}} SOURCES)
	foreach(source ${{target_sources}})
		if(source MATCHES "\\.(h|hpp)$")
			get_filename_component(directory ${{source}} DIRECTORY)
			get_filename_component(filename ${{source}} NAME_WE)
			get_filename_component(ext ${{source}} EXT)
			set(moc_input "${{directory}}/${{filename}}${{ext}}")
			file(RELATIVE_PATH rel_directory ${{CMAKE_CURRENT_SOURCE_DIR}} ${{directory}})
			set(moc_output "${{CMAKE_CURRENT_BINARY_DIR}}/${{rel_directory}}/moc_${{filename}}.cpp")
			set(moc_includes "$<LIST:TRANSFORM,$<TARGET_PROPERTY:third_k_editor_objects,INTERFACE_INCLUDE_DIRECTORIES>,PREPEND,-I>")

            file(RELATIVE_PATH rel_moc_input "${{CMAKE_SOURCE_DIR}}" "${{moc_input}}")

			add_custom_command(
					OUTPUT ${{moc_output}}
					COMMAND ${{IPRM_QT_MOC_EXECUTABLE}}
					${{moc_includes}}
					${{moc_input}}
					-o ${{moc_output}}
					DEPENDS
					${{source}} ${{unpack_target}}
					COMMENT "MOC ${{rel_moc_input}}"
					VERBATIM
					COMMAND_EXPAND_LISTS
			)
			target_sources(${{target}} PRIVATE ${{moc_output}})
		endif()
	endforeach()
endfunction()

{self._cmake_qt_autorcc()}

{self._cmake_qt_autouic()}
""")
        return cmake_content

    def _generate_cmake_qt_pkgconfig(self, cpp_third: QtThirdParty):
        cmake_content = []
        if not self._cmake_qt_utils_module_file().parent.exists():
            self._cmake_qt_utils_module_file().parent.mkdir(parents=True)
        # TODO: Maybe use python pkg-config library instead so each target that includes the
        #   qt utils doesn't need to invoke the process, that way we can just hardcode the
        #   module file. That being said, it is cheap/quick, so this is fine for now
        self._cmake_qt_utils_module_file().write_text(f"""{self._backend.current_generated_file_header}                          
execute_process(
    COMMAND bash -c "dirname $($(pkg-config --variable=bindir Qt6Core)/qmake -query QT_INSTALL_PLUGINS)"
    OUTPUT_VARIABLE PKCONFIG_QT_ROOT_DIR
    OUTPUT_STRIP_TRAILING_WHITESPACE
)
execute_process(
  COMMAND pkg-config --variable=libexecdir Qt6Core
  OUTPUT_VARIABLE QT6_LIBEXECDIR
  OUTPUT_STRIP_TRAILING_WHITESPACE
)
set(IPRM_QT_ROOT_DIR "${{PKCONFIG_QT_ROOT_DIR}}" CACHE PATH "Root Qt Directory")
set(IPRM_QT_MOC_EXECUTABLE "${{QT6_LIBEXECDIR}}/moc" CACHE PATH "Qt MOC Executable")
set(IPRM_QT_RCC_EXECUTABLE "${{QT6_LIBEXECDIR}}/rcc" CACHE PATH "Qt RCC Executable")
set(IPRM_QT_UIC_EXECUTABLE "${{QT6_LIBEXECDIR}}/uic" CACHE PATH "Qt UIC Executable")

{self._cmake_qt_automoc()}

# Source archive specific automoc helper fixing issue with CMake having to generate its target build system file(s) 
# twice, at least with Ninja, for the headers to actually get MOC'd
function(iprm_qt_automoc_source_archive target unpack_target)
	get_target_property(target_sources ${{target}} SOURCES)
	foreach(source ${{target_sources}})
		if(source MATCHES "\\.(h|hpp)$")
			get_filename_component(directory ${{source}} DIRECTORY)
			get_filename_component(filename ${{source}} NAME_WE)
			get_filename_component(ext ${{source}} EXT)
			set(moc_input "${{directory}}/${{filename}}${{ext}}")
			file(RELATIVE_PATH rel_directory ${{CMAKE_CURRENT_SOURCE_DIR}} ${{directory}})
			set(moc_output "${{CMAKE_CURRENT_BINARY_DIR}}/${{rel_directory}}/moc_${{filename}}.cpp")
			set(moc_includes "$<LIST:TRANSFORM,$<TARGET_PROPERTY:third_k_editor_objects,INTERFACE_INCLUDE_DIRECTORIES>,PREPEND,-I>")

            file(RELATIVE_PATH rel_moc_input "${{CMAKE_SOURCE_DIR}}" "${{moc_input}}")

			add_custom_command(
					OUTPUT ${{moc_output}}
					COMMAND ${{IPRM_QT_MOC_EXECUTABLE}}
					${{moc_includes}}
					${{moc_input}}
					-o ${{moc_output}}
					DEPENDS
					${{source}} ${{unpack_target}}
					COMMENT "MOC ${{rel_moc_input}}"
					VERBATIM
					COMMAND_EXPAND_LISTS
			)
			target_sources(${{target}} PRIVATE ${{moc_output}})
		endif()
	endforeach()
endfunction()

{self._cmake_qt_autorcc()}

{self._cmake_qt_autouic()}
""")
        return cmake_content

    @classmethod
    def _cmake_qt_automoc(cls):
        return f"""function(iprm_qt_automoc target)
    get_target_property(target_sources ${{target}} SOURCES)
    set(headers_to_moc "")
    
    set(moc_includes "$<LIST:TRANSFORM,$<TARGET_PROPERTY:${{target}},INTERFACE_INCLUDE_DIRECTORIES>,PREPEND,-I>")
    
    foreach(source_file ${{target_sources}})
        if(source_file MATCHES "\\\\.(h|hpp|hxx)$")
            if(IS_ABSOLUTE ${{source_file}})
                set(header_path "${{source_file}}")
            else()
                set(header_path "${{CMAKE_CURRENT_SOURCE_DIR}}/${{source_file}}")
            endif()
    
            if(EXISTS "${{header_path}}")
                file(READ "${{header_path}}" header_contents)
                if(header_contents MATCHES "Q_OBJECT")
                    list(APPEND headers_to_moc "${{header_path}}")
                endif()
            endif()
        endif()
    endforeach()
    
    foreach(header_path ${{headers_to_moc}})
        get_filename_component(header_name_we ${{header_path}} NAME_WE)
        set(moc_file "${{CMAKE_CURRENT_BINARY_DIR}}/moc_${{header_name_we}}.cpp")
    
        file(RELATIVE_PATH rel_header_path "${{CMAKE_SOURCE_DIR}}" "${{header_path}}")
    
        add_custom_command(
                OUTPUT ${{moc_file}}
                COMMAND ${{IPRM_QT_MOC_EXECUTABLE}}
                ARGS ${{moc_includes}} -o ${{moc_file}} ${{header_path}}
                DEPENDS ${{header_path}} ${{IPRM_QT_UNPACK_TARGET_NAME}}
                COMMENT "MOC ${{rel_header_path}}"
                VERBATIM
                COMMAND_EXPAND_LISTS
        )
        target_sources(${{target}} PRIVATE ${{moc_file}})
    endforeach()
endfunction()
"""

    @classmethod
    def _cmake_qt_autorcc(cls):
        return f"""function(iprm_qt_autorcc target)
    get_target_property(target_sources ${{target}} SOURCES)
    foreach(source_file ${{target_sources}})
        if(source_file MATCHES "\\\\.qrc$")
            if(IS_ABSOLUTE ${{source_file}})
                set(qrc_file "${{source_file}}")
            else()
                set(qrc_file "${{CMAKE_CURRENT_SOURCE_DIR}}/${{source_file}}")
            endif()
    
            get_filename_component(qrc_name_we ${{qrc_file}} NAME_WE)
            set(rcc_cpp_file "${{CMAKE_CURRENT_BINARY_DIR}}/qrc_${{qrc_name_we}}.cpp")
            
            file(RELATIVE_PATH rel_qrc_file "${{CMAKE_SOURCE_DIR}}" "${{qrc_file}}")
    
            add_custom_command(
                    OUTPUT ${{rcc_cpp_file}}
                    COMMAND ${{IPRM_QT_RCC_EXECUTABLE}}
                    ARGS -name ${{qrc_name_we}} -o ${{rcc_cpp_file}} ${{qrc_file}}
                    DEPENDS ${{qrc_file}} ${{IPRM_QT_UNPACK_TARGET_NAME}}
                    COMMENT "RCC ${{rel_qrc_file}}"
                    VERBATIM
            )
            target_sources(${{target}} PRIVATE ${{rcc_cpp_file}})
        endif()
    endforeach()
endfunction()
"""

    @classmethod
    def _cmake_qt_autouic(cls):
        return f"""function(iprm_qt_autouic target)
    get_target_property(target_sources ${{target}} SOURCES)
    foreach(source_file ${{target_sources}})
        if(source_file MATCHES "\\\\.ui$")
            if(IS_ABSOLUTE ${{source_file}})
                set(ui_file "${{source_file}}")
            else()
                set(ui_file "${{CMAKE_CURRENT_SOURCE_DIR}}/${{source_file}}")
            endif()
    
            get_filename_component(ui_name_we ${{ui_file}} NAME_WE)
            set(ui_h_file "${{CMAKE_CURRENT_BINARY_DIR}}/ui_${{ui_name_we}}.h")
    
            file(RELATIVE_PATH rel_ui_file "${{CMAKE_SOURCE_DIR}}" "${{ui_file}}")
    
            add_custom_command(
                    OUTPUT ${{ui_h_file}}
                    COMMAND ${{IPRM_QT_UIC_EXECUTABLE}}
                    ARGS -o ${{ui_h_file}} ${{ui_file}}
                    DEPENDS ${{ui_file}} ${{IPRM_QT_UNPACK_TARGET_NAME}}
                    COMMENT "UIC ${{rel_ui_file}}"
                    VERBATIM
            )
            target_include_directories(${{target}} PRIVATE ${{CMAKE_CURRENT_BINARY_DIR}})
    
            set_property(TARGET ${{target}} APPEND PROPERTY ADDITIONAL_CLEAN_FILES ${{ui_h_file}})
            add_custom_target(
                    ${{target}}_ui_${{ui_name_we}} ALL DEPENDS ${{ui_h_file}}
            )
            add_dependencies(${{target}} ${{target}}_ui_${{ui_name_we}})
        endif()
    endforeach()
endfunction()
"""

    # TODO: Nothing is actually testing the meson Qt generation currently (as IPRM Studio only has CMake backend
    #  support), need to add a simple Qt GUI application to the CLI Testsuite to ensure this actually works
    #  properly. Right now it most likely doesn't as object generator plugins right now are only invoked after the main
    #  object generation is done. So we may need to allow for ObjectGenerator's to override an entire objects generation
    #  for scenarios like Meson due to how we specify the moc/rcc/uic generated sources for a given target

    def _generate_meson_qt_first_party(self, cpp: CppTarget, qt_third: QtThirdParty):
        return self._generate_meson_qt_sources(cpp, qt_third)

    def _generate_meson_qt_third_party(self, cpp_third: CppThirdParty, qt_third: Optional[QtThirdParty]):
        if qt_third and cpp_third.is_source_archive:
            # TODO: Get Meson source archive custom target infrastructure working so IPRM Studio can also be built with Meson
            """
            return self._generate_meson_qt_sources(cpp_third, qt_third,
                                                   target=cpp_third.properties.get('build_target', None))
            """
            pass
        cpp_qt_third = cast(QtThirdParty, cpp_third)
        if cpp_third.is_precompiled_archive:
            return self._generate_cmake_qt_precompiled_archive(cpp_qt_third)
        # TODO: Support other third party content types
        return []

    def _generate_meson_qt_sources(self, cpp: CppTarget, qt_third: QtThirdParty, target=None):
        meson_content = []
        meson_backend = cast(Meson, self._backend)
        generated_source_files = []
        header_files = meson_backend.cpp_get_header_src_file_paths(cpp)
        source_files = meson_backend.cpp_get_source_src_file_paths(cpp)
        if qt_third.properties.get(QtThirdParty.MOC, False):
            target_moc_headers = f'{target}_moc_headers'
            meson_content.append(f'{target_moc_headers} = [')
            if header_files:
                for header_file in header_files:
                    meson_content.append(f'\t{header_file},')
                meson_content.append(']')
            else:
                meson_content[-1] += ']'
            header_files.clear()
            target_moc_sources = f'{target}_moc_sources'
            meson_content.append(f'{target_moc_sources} = iprm_moc_generator.process({target_moc_headers})')
            generated_source_files.append(target_moc_headers)
            generated_source_files.append(target_moc_sources)
        if qt_third.properties.get(QtThirdParty.RCC, False):
            target_qrc_files = f'{target}_qrc_files'
            qrc_files = meson_backend._cpp_get_sources(cpp, 'sources', ['qrc'], meson_backend.relative_src_path)
            source_files = [file for file in source_files if file not in qrc_files]
            meson_content.append(f'{target_qrc_files} = [')
            if qrc_files:
                for qrc_file in qrc_files:
                    meson_content.append(f'\t{qrc_file},')
                meson_content.append(']')
            else:
                meson_content[-1] += ']'
            target_qrc_sources = f'{target}_qrc_sources'
            meson_content.append(f'{target_qrc_sources} = iprm_rcc_generator.process({target_qrc_files})')
            generated_source_files.append(target_qrc_sources)
        if qt_third.properties.get(QtThirdParty.UIC, False):
            target_ui_files = f'{target}_ui_files'
            ui_files = meson_backend._cpp_get_sources(cpp, 'sources', ['ui'], meson_backend.relative_src_path)
            source_files = [file for file in source_files if file not in ui_files]
            meson_content.append(f'{target_ui_files} = [')
            if ui_files:
                for ui_file in ui_files:
                    meson_content.append(f'\t{ui_file},')
                meson_content.append(']')
            else:
                meson_content[-1] += ']'
            target_ui_sources = f'{target}_ui_sources'
            meson_content.append(f'{target_ui_sources} = iprm_uic_generator.process({target_ui_files})')
            generated_source_files.append(target_ui_sources)
        if qt_third.properties.get(QtThirdParty.CONF, False):
            qt_conf_content = f"""{self._backend.current_generated_file_header}
[Paths]
Prefix=@IPRM_QT_ROOT_DIR@
Plugins=@IPRM_QT_ROOT_DIR@/plugins
"""
            qt_conf_template_file = self._backend.current_generate_dir / 'qt.conf.in'
            qt_conf_template_file.write_text(qt_conf_content)
            meson_content.append('qt_conf_data = configuration_data()')
            meson_content.append(
                f"qt_conf_data.set('IPRM_QT_ROOT_DIR', meson.project_build_root() / '{qt_third.root_relative_dir.path.as_posix()}')")
            meson_content.append('configure_file(')
            meson_content.append("\tinput: 'qt.conf.in',")
            meson_content.append("\toutput: 'qt.conf',")
            meson_content.append("\tconfiguration: qt_conf_data,")
            meson_content.append(')')

            # TODO: generated sources need to be attached to the target
            # generated_source_files
        return meson_content

    def _generate_meson_qt_precompiled_archive(self, cpp: CppTarget, unpack_target_name: str):
        meson_content = []
        meson_backend = cast(Meson, self._backend)
        qt_utils_file_path = self._backend.current_generate_dir / 'meson_qt_utils.py'
        with qt_utils_file_path.open(mode='a') as qt_utils_file:
            qt_utils_file.write(f"""{self._backend.current_generated_file_header}
import os
import sys
import subprocess

# First argument is the absolute path to the executable
if len(sys.argv) < 2:
    print("Usage: wrapper.py <executable_path> [arguments...]")
    sys.exit(1)

executable_path = sys.argv[1]
args = sys.argv[2:]

# Check if Qt directory exists
qt_bin_dir = os.path.dirname(executable_path)
if not os.path.exists(qt_bin_dir):
    print(f"Error: Qt binary directory '{{qt_bin_dir}}' does not exist")
    sys.exit(1)

# Forward all remaining arguments to the actual executable
cmd = [executable_path] + args
try:
    result = subprocess.run(cmd)
    sys.exit(result.returncode)
except FileNotFoundError:
    print(f"Error: Executable '{{executable_path}}' not found")
    sys.exit(1)
""")
        meson_content.append(f"meson_qt_utils = {meson_backend.current_src_dir()} / 'meson_qt_utils.py'")
        meson_content.append(
            f"iprm_qt_root_dir = meson.project_build_root() / '{cpp.root_relative_dir.path.as_posix()}'")
        meson_content.append(f"iprm_qt_bin_dir = iprm_qt_root_dir / '{cpp.properties.get('bin_dir').path.as_posix()}'")
        meson_content.append(f"{meson_backend.MESON_RUN_ENV}.prepend('PATH', iprm_qt_bin_dir)")
        meson_content.append(f"iprm_qt_moc = iprm_qt_bin_dir / '{QtThirdParty.MOC}'")
        meson_content.append(f"""iprm_moc_generator = generator(
  python,
  output: 'moc_@BASENAME@.cpp',
  arguments: [meson_qt_utils, iprm_qt_moc, '@INPUT@', '-o', '@OUTPUT@'],
  depends: [{unpack_target_name}],
)
""")
        meson_content.append(f"iprm_qt_rcc = iprm_qt_bin_dir / '{QtThirdParty.RCC}'")
        meson_content.append(f"""iprm_rcc_generator = generator(
  python,
  output: 'qrc_@BASENAME@.cpp',
  arguments: [meson_qt_utils, iprm_qt_rcc, '@INPUT@', '-o', '@OUTPUT@'],
  depends: [{unpack_target_name}],
)
""")
        meson_content.append(f"iprm_qt_uic = iprm_qt_bin_dir / '{QtThirdParty.UIC}'")
        meson_content.append(f"""iprm_uic_generator = generator(
  python,
  output: 'ui_@BASENAME@.h',
  arguments: [meson_qt_utils, iprm_qt_uic, '@INPUT@', '-o', '@OUTPUT@'],
  depends: [{unpack_target_name}],
)
""")
        return meson_content
