import importlib
import inspect
import sys
from pathlib import Path
from iprm.util.env import Env
from iprm.backend.backend import Backend
from iprm.core.object import Object


def _load_plugins(plugin_dir, plugin_type):
    loaded_plugins = {}
    plugin_path = Path(plugin_dir)

    if not plugin_path.is_dir():
        raise ValueError(f"Directory not found: {plugin_path}")

    str_plugin_dir = str(plugin_path.absolute())
    if str_plugin_dir not in sys.path:
        sys.path.insert(0, str_plugin_dir)

    for file_path in plugin_path.rglob('*.py'):
        if not file_path.is_file():
            continue

        relative_path = file_path.relative_to(plugin_path)
        module_name = '.'.join(relative_path.parent.parts + (relative_path.stem,))

        try:
            module = importlib.import_module(module_name)
            for name, obj in inspect.getmembers(module):
                if (getattr(obj, '__module__', None) == module_name and
                    inspect.isclass(obj) and
                    issubclass(obj, plugin_type) and
                    obj != plugin_type and
                    obj.__module__ == module_name and
                        (Env.platform in obj.platforms() if hasattr(obj, 'platforms') else True)
                ):
                    obj_name = obj.__name__
                    print(f"{plugin_type.__name__} plugin '{module_name}.{obj_name}' loaded from {file_path}")
                    loaded_plugins[obj_name] = obj

        except (ImportError, AttributeError):
            pass

    if str_plugin_dir in sys.path:
        sys.path.remove(str_plugin_dir)
    return loaded_plugins


def load_backends(plugin_dir):
    return _load_plugins(plugin_dir, Backend)


def load_objects(plugin_dir):
    return _load_plugins(plugin_dir, Object)
