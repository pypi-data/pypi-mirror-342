from abc import abstractmethod, ABC
from pathlib import Path


class Dir(ABC):
    def __init__(self, path):
        self.path = path

    @abstractmethod
    def __hash__(self):
        pass

    @abstractmethod
    def __eq__(self, other):
        pass

    @property
    @abstractmethod
    def binary(self):
        pass

    def prepend(self, *path):
        self.path = Path(*path) / self.path


class _CurrentDir(Dir):
    def __init__(self):
        super().__init__(Path('.'))

    def __hash__(self):
        return hash(self.path)

    def __eq__(self, other):
        if not isinstance(other, _CurrentDir):
            return False
        return True


class CurrentSourceDir(_CurrentDir):
    @property
    def binary(self):
        return False


class _Dir(Dir):
    def __init__(self, *path):
        super().__init__(Path(*path))

    def __hash__(self):
        return hash(self.path)

    def __eq__(self, other: Dir):
        return self.path == other.path


class SourceDir(_Dir):
    @property
    def binary(self):
        return False


class RootRelativeSourceDir(SourceDir):
    def __init__(self, *path):
        super().__init__(*path)
        from iprm.core.session import Session
        # TODO: Rename to root_relative_dir
        self.path = Path(Session.root_relative_source_dir()) / self.path


class CurrentBinaryDir(_CurrentDir):
    @property
    def binary(self):
        return True


class BinaryDir(_Dir):
    @property
    def binary(self):
        return True

class RootRelativeBinaryDir(SourceDir):
    def __init__(self, *path):
        super().__init__(*path)
        from iprm.core.session import Session
        self.path = Path(Session.root_relative_source_dir()) / self.path
