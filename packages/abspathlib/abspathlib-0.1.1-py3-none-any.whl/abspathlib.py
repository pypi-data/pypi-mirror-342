import os
import shutil
import fnmatch

def split_path(path):
    if path:
        if '//' in path:
            raise Exception('Path has empty parts')
        if path == os.path.sep:
            parts = [os.path.sep]
        elif path.startswith(os.path.sep):
            parts = [os.path.sep] + path[1:].split(os.path.sep)
        else:
            parts = path.split(os.path.sep)
        return parts
    else:
        return []

class NotAbsolutePathError(ValueError):
    pass

class AbsPath(str):
    def __new__(cls, path='/', relto=None):
        if not isinstance(path, str):
            raise TypeError('Path must be a string')
        if not path:
            raise ValueError('Path can not be empty')
        if relto is None:
            if not os.path.isabs(path):
                raise NotAbsolutePathError
        elif not os.path.isabs(path):
            if not isinstance(relto, str):
                raise TypeError('Parent directory must be a string')
            if not os.path.isabs(relto):
                raise ValueError('Parent directory must be an absolute path')
            path = os.path.join(relto, path)
        obj = str.__new__(cls, path)
        obj.parts = tuple(split_path(obj))
        obj.name = os.path.basename(obj)
        obj.stem, obj.suffix = os.path.splitext(obj.name)
        return obj

    def __mod__(self, right):
        if not isinstance(right, str):
            print(type(right))
            raise TypeError('Right operand must be a string')
        if '/' in right:
            raise ValueError('Can not use a path as an extension')
        return AbsPath(self.name + '.' + right, relto=self.parent)

    def __truediv__(self, right):
        if not isinstance(right, str):
            raise TypeError('Right operand must be a string')
        if isinstance(right, AbsPath):
            raise ValueError('Can not join two absolute paths')
        return AbsPath(right, relto=self)

    @property
    def parent(self):
        """Return the parent directory as a new AbsPath object."""
        return AbsPath(os.path.dirname(self))

    def parents(self):
        """Return an iterator of all parents of this path."""
        path = self
        while len(path.parts) > 1:
            path = path.parent
            yield path

    def iterdir(self):
        """Iterate over the files in this directory."""
        if not self.is_dir():
            raise NotADirectoryError(f"{self} is not a directory")
        with os.scandir(self) as it:
            for entry in it:
                yield AbsPath(entry.path)

    def listdir(self):
        """Return a list of filenames in this directory."""
        return os.listdir(self)

    def has_suffix(self, suffix):
        """Check if the file has the specified suffix."""
        return self.suffix == suffix

    def exists(self):
        """Return True if the path exists."""
        return os.path.exists(self)

    def is_file(self):
        """Return True if the path points to a regular file."""
        return os.path.isfile(self)

    def is_dir(self):
        """Return True if the path points to a directory."""
        return os.path.isdir(self)

    def is_symlink(self):
        """Return True if the path points to a symbolic link."""
        return os.path.islink(self)

    def unlink(self, missing_ok=False):
        """Remove this file or symbolic link."""
        try:
            os.remove(self)
        except FileNotFoundError:
            if not missing_ok:
                raise

    def rmdir(self):
        """Remove this directory."""
        try:
            os.rmdir(self)
        except FileNotFoundError:
            raise

    def mkdir(self, mode=0o777, parents=False, exist_ok=False):
        """Create a new directory at this path."""
        try:
            if parents:
                os.makedirs(self, mode=mode, exist_ok=exist_ok)
            else:
                os.mkdir(self, mode=mode)
        except FileExistsError:
            if exist_ok and os.path.isdir(self):
                pass
            else:
                raise

    def chmod(self, mode):
        """Change file mode bits."""
        os.chmod(self, mode)

    def copy(self, target):
        """Copy this file to target, preserving file attributes."""
        shutil.copy(self, target)

    def copyfile(self, target):
        """Copy this file to target without preserving file attributes."""
        shutil.copyfile(self, target)

    def rename(self, target):
        """Rename this file or directory to the given target."""
        os.rename(self, target)

    def replace(self, target):
        """Replace target with this file/directory."""
        os.replace(self, target)

    def symlink_to(self, target):
        """Create a symbolic link pointing to target."""
        os.symlink(target, self)

    def readlink(self):
        """Return the path to which the symbolic link points.

        Unlike pathlib.Path.readlink(), this returns an AbsPath that's
        already resolved and absolute. To get behavior closer to pathlib's,
        use readlink() without resolving the result.
        """
        return AbsPath(os.readlink(self))

    def iterglob(self, pattern):
        """Return an iterator of paths matching the given pattern."""
        with os.scandir(self) as it:
            for entry in it:
                if fnmatch.fnmatch(entry.name, pattern):
                    yield AbsPath(entry.path)

    def riterglob(self, pattern):
        """Recursively match the given pattern in this directory tree."""
        for dirpath, dirnames, filenames in os.walk(self):
            base_path = AbsPath(dirpath)
            for name in dirnames + filenames:
                if fnmatch.fnmatch(name, pattern):
                    yield base_path / name

    def listglob(self, pattern):
        return fnmatch.filter(os.listdir(self), pattern)

    def assert_file(self):
        """Assert that this path is a file."""
        if os.path.exists(self):
            if not os.path.isfile(self):
                if os.path.isdir(self):
                    raise IsADirectoryError
                else:
                    raise OSError(f'{self} no es un archivo regular')
        else:
            raise FileNotFoundError

    def assert_dir(self):
        """Assert that this path is a directory."""
        if os.path.exists(self):
            if os.path.isfile(self):
                raise NotADirectoryError
        else:
            raise FileNotFoundError

    def stat(self):
        """Return the stat result of this path."""
        return os.stat(self)

    def lstat(self):
        """Return the stat result of this path (not following symlinks)."""
        return os.lstat(self)

    def owner(self):
        """Return the name of the owner of this file."""
        import pwd
        return pwd.getpwuid(self.stat().st_uid).pw_name

    def group(self):
        """Return the name of the group owner of this file."""
        import grp
        return grp.getgrgid(self.stat().st_gid).gr_name

    def is_absolute(self):
        """Return True if this path is absolute."""
        return os.path.isabs(self)

    def is_reserved(self):
        """Return True if this path is a reserved path on Windows."""
        # Not applicable on non-Windows systems
        return False

    def joinpath(self, *paths):
        """Combine this path with the given paths."""
        result = self
        for path in paths:
            result = result / path
        return result

    def with_name(self, name):
        """Return a new path with the name changed."""
        return AbsPath(os.path.join(os.path.dirname(self), name))

    def with_suffix(self, suffix):
        """Return a new path with the suffix changed."""
        if not suffix.startswith('.'):
            suffix = '.' + suffix
        return AbsPath(os.path.join(os.path.dirname(self), self.stem + suffix))

    def resolve(self):
        """Make the path absolute and resolve any symlinks."""
        return AbsPath(os.path.realpath(self))

    def expanduser(self):
        """Expand ~ and ~user to the user's home directory."""
        return AbsPath(os.path.expanduser(self))
