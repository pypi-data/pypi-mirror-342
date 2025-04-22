"""
Filesystem based backend implementation - uses files in directories below a base path.
"""

import os
import re
import sys
from pathlib import Path
import shutil
import stat
import tempfile

from ._base import BackendBase, ItemInfo, validate_name
from .errors import BackendError, BackendAlreadyExists, BackendDoesNotExist, BackendMustNotBeOpen, BackendMustBeOpen
from .errors import ObjectNotFound
from ..constants import TMP_SUFFIX


def get_file_backend(url):
    # file:///absolute/path
    # notes:
    # - we only support **local** fs **absolute** paths.
    # - there is no such thing as a "relative path" local fs file: url
    # - the general url syntax is proto://host/path
    # - // introduces the host part. it is empty here, meaning localhost / local fs.
    # - the third slash is NOT optional, it is the start of an absolute path as well
    #   as the separator between the host and the path part.
    # - the caller is responsible to give an absolute path.
    # - windows: see there: https://en.wikipedia.org/wiki/File_URI_scheme
    windows_file_regex = r"""
        file://  # only empty host part is supported.
        /  # 3rd slash is separator ONLY, not part of the path.
        (?P<drive_and_path>([a-zA-Z]:/.*))  # path must be an absolute path.
    """
    file_regex = r"""
        file://  # only empty host part is supported.
        (?P<path>(/.*))  # path must be an absolute path. 3rd slash is separator AND part of the path.
    """
    if sys.platform in ("win32", "msys", "cygwin"):
        m = re.match(windows_file_regex, url, re.VERBOSE)
        if m:
            return PosixFS(path=m["drive_and_path"])
    m = re.match(file_regex, url, re.VERBOSE)
    if m:
        return PosixFS(path=m["path"])


class PosixFS(BackendBase):
    # PosixFS implementation supports precreate = True as well as = False.
    precreate_dirs: bool = False

    def __init__(self, path, *, do_fsync=False):
        self.base_path = Path(path)
        if not self.base_path.is_absolute():
            raise BackendError("path must be an absolute path")
        self.opened = False
        self.do_fsync = do_fsync  # False = 26x faster, see #10

    def create(self):
        if self.opened:
            raise BackendMustNotBeOpen()
        # we accept an already existing empty directory and we also optionally create
        # any missing parent dirs. the latter is important for repository hosters that
        # only offer limited access to their storage (e.g. only via borg/borgstore).
        # also, it is simpler than requiring users to create parent dirs separately.
        self.base_path.mkdir(exist_ok=True, parents=True)
        # avoid that users create a mess by using non-empty directories:
        contents = list(self.base_path.iterdir())
        if contents:
            raise BackendAlreadyExists(f"posixfs storage base path is not empty: {self.base_path}")

    def destroy(self):
        if self.opened:
            raise BackendMustNotBeOpen()
        try:
            shutil.rmtree(os.fspath(self.base_path))
        except FileNotFoundError:
            raise BackendDoesNotExist(f"posixfs storage base path does not exist: {self.base_path}")

    def open(self):
        if self.opened:
            raise BackendMustNotBeOpen()
        if not self.base_path.is_dir():
            raise BackendDoesNotExist(
                f"posixfs storage base path does not exist or is not a directory: {self.base_path}"
            )
        self.opened = True

    def close(self):
        if not self.opened:
            raise BackendMustBeOpen()
        self.opened = False

    def _validate_join(self, name):
        validate_name(name)
        return self.base_path / name

    def mkdir(self, name):
        if not self.opened:
            raise BackendMustBeOpen()
        path = self._validate_join(name)
        path.mkdir(parents=True, exist_ok=True)

    def rmdir(self, name):
        if not self.opened:
            raise BackendMustBeOpen()
        path = self._validate_join(name)
        try:
            path.rmdir()
        except FileNotFoundError:
            raise ObjectNotFound(name) from None

    def info(self, name):
        if not self.opened:
            raise BackendMustBeOpen()
        path = self._validate_join(name)
        try:
            st = path.stat()
        except FileNotFoundError:
            return ItemInfo(name=path.name, exists=False, directory=False, size=0)
        else:
            is_dir = stat.S_ISDIR(st.st_mode)
            return ItemInfo(name=path.name, exists=True, directory=is_dir, size=st.st_size)

    def load(self, name, *, size=None, offset=0):
        if not self.opened:
            raise BackendMustBeOpen()
        path = self._validate_join(name)
        try:
            with path.open("rb") as f:
                if offset > 0:
                    f.seek(offset)
                return f.read(-1 if size is None else size)
        except FileNotFoundError:
            raise ObjectNotFound(name) from None

    def store(self, name, value):
        def _write_to_tmpfile():
            with tempfile.NamedTemporaryFile(suffix=TMP_SUFFIX, dir=tmp_dir, delete=False) as f:
                f.write(value)
                if self.do_fsync:
                    f.flush()
                    os.fsync(f.fileno())
                tmp_path = Path(f.name)
            return tmp_path

        if not self.opened:
            raise BackendMustBeOpen()
        path = self._validate_join(name)
        tmp_dir = path.parent
        # write to a differently named temp file in same directory first,
        # so the store never sees partially written data.
        try:
            # try to do it quickly, not doing the mkdir. fs ops might be slow, esp. on network fs (latency).
            # this will frequently succeed, because the dir is already there.
            tmp_path = _write_to_tmpfile()
        except FileNotFoundError:
            # retry, create potentially missing dirs first. this covers these cases:
            # - either the dirs were not precreated
            # - a previously existing directory was "lost" in the filesystem
            tmp_dir.mkdir(parents=True, exist_ok=True)
            tmp_path = _write_to_tmpfile()
        # all written and synced to disk, rename it to the final name:
        try:
            tmp_path.replace(path)
        except OSError:
            tmp_path.unlink()
            raise

    def delete(self, name):
        if not self.opened:
            raise BackendMustBeOpen()
        path = self._validate_join(name)
        try:
            path.unlink()
        except FileNotFoundError:
            raise ObjectNotFound(name) from None

    def move(self, curr_name, new_name):
        def _rename_to_new_name():
            curr_path.rename(new_path)

        if not self.opened:
            raise BackendMustBeOpen()
        curr_path = self._validate_join(curr_name)
        new_path = self._validate_join(new_name)
        try:
            # try to do it quickly, not doing the mkdir. fs ops might be slow, esp. on network fs (latency).
            # this will frequently succeed, because the dir is already there.
            _rename_to_new_name()
        except FileNotFoundError:
            # retry, create potentially missing dirs first. this covers these cases:
            # - either the dirs were not precreated
            # - a previously existing directory was "lost" in the filesystem
            new_path.parent.mkdir(parents=True, exist_ok=True)
            try:
                _rename_to_new_name()
            except FileNotFoundError:
                raise ObjectNotFound(curr_name) from None

    def list(self, name):
        if not self.opened:
            raise BackendMustBeOpen()
        path = self._validate_join(name)
        try:
            paths = sorted(path.iterdir())
        except FileNotFoundError:
            raise ObjectNotFound(name) from None
        else:
            for p in paths:
                if not p.name.endswith(TMP_SUFFIX):
                    try:
                        st = p.stat()
                    except FileNotFoundError:
                        pass
                    else:
                        is_dir = stat.S_ISDIR(st.st_mode)
                        yield ItemInfo(name=p.name, exists=True, size=st.st_size, directory=is_dir)
