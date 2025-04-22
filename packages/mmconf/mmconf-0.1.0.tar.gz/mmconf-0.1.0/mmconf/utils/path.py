from pathlib import Path

from .misc import is_str


def check_file_exist(filename, msg_tmpl='file "{}" does not exist'):
    filename = Path(filename)
    if filename.is_file():
        raise FileNotFoundError(msg_tmpl.format(filename))


def is_filepath(x):
    return is_str(x) or isinstance(x, Path)


def fopen(filepath, *args, **kwargs):
    if is_str(filepath):
        return open(filepath, *args, **kwargs)
    elif isinstance(filepath, Path):
        return filepath.open(*args, **kwargs)
    raise ValueError('`filepath` should be a string or a Path')


def mkdir_or_exist(dir_name, mode=0o777):
    if dir_name == '':
        return
    dir_name = Path(dir_name).expanduser()
    dir_name.mkdir(parents=True, exist_ok=True)


def symlink(src, dst, overwrite=True, **kwargs):
    dst = Path(dst)
    if dst.exists(follow_symlinks=False) and not overwrite:
        raise FileExistsError(f'{dst} already exists, set `overwrite=True` to overwrite it')
    dst.symlink_to(src, **kwargs)


def scandir(dir_path, suffix=None, recursive=False, case_sensitive=True):
    """Scan a directory to find the interested files.

    Args:
        dir_path (str | :obj:`Path`): Path of the directory.
        suffix (str | tuple(str), optional): File suffix that we are
            interested in. Defaults to None.
        recursive (bool, optional): If set to True, recursively scan the
            directory. Defaults to False.
        case_sensitive (bool, optional) : If set to False, ignore the case of
            suffix. Defaults to True.

    Returns:
        A generator for all the interested files with relative paths.
    """
    if isinstance(dir_path, (str, Path)):
        dir_path = str(dir_path)
    else:
        raise TypeError('"dir_path" must be a string or Path object')

    if (suffix is not None) and not isinstance(suffix, (str, tuple)):
        raise TypeError('"suffix" must be a string or tuple of strings')

    if suffix is not None and not case_sensitive:
        suffix = suffix.lower() if isinstance(suffix, str) else tuple(
            item.lower() for item in suffix)

    root = dir_path

    def _scandir(dir_path, suffix, recursive, case_sensitive):
        for entry in Path(dir_path).iterdir():
            if not entry.name.startswith('.') and entry.is_file():
                rel_path = str(entry.relative_to(root))
                _rel_path = rel_path if case_sensitive else rel_path.lower()
                if suffix is None or _rel_path.endswith(suffix):
                    yield rel_path
            # elif recursive and os.path.isdir(entry.path):
            elif recursive and entry.is_dir():
                # scan recursively if entry.path is a directory
                yield from _scandir(str(entry), suffix, recursive,
                                    case_sensitive)

    return _scandir(dir_path, suffix, recursive, case_sensitive)


def find_vcs_root(path, markers=('.git', )):
    """Finds the root directory (including itself) of specified markers.

    Args:
        path (str): Path of directory or file.
        markers (list[str], optional): List of file or directory names.

    Returns:
        The directory contained one of the markers or None if not found.
    """
    path = Path(path)
    if path.is_file():
        path = path.parent

    prev, cur = None, path.expanduser().resolve()
    while cur != prev:
        if any(((Path(cur) / marker).exists()) for marker in markers):
            return cur
        prev, cur = cur, cur.parent
    return None


def is_abs(path: str) -> bool:
    """Check if path is an absolute path in different backends.

    Args:
        path (str): path of directory or file.

    Returns:
        bool: whether path is an absolute path.
    """
    if Path(path).is_absolute() or path.startswith(('http://', 'https://', 's3://')):
        return True
    else:
        return False
