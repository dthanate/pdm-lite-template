import pickle
from os import PathLike
from pathlib import Path
from typing import BinaryIO
from typing import cast
from typing import Optional

import dill.settings
import fsspec
from fsspec.core import OpenFile
from fsspec.spec import AbstractFileSystem


def __dill_load(fhandle: BinaryIO) -> object:
    return dill.load(
        fhandle,
        ignore=True,
        byref=True,
        recurse=True,
        fix_imports=False,
    )


def __pickle_load(fhandle: BinaryIO) -> object:
    return pickle.load(
        fhandle,
        fix_imports=False,
    )


def __dill_dump(
    obj: object,
    fhandle: BinaryIO,
    protocol: int,
) -> None:
    dill.dump(
        obj,
        fhandle,
        protocol=protocol,
        byref=True,
        recurse=True,
        fix_imports=False,
    )


def __pickle_dump(
    obj: object,
    fhandle: BinaryIO,
    protocol: int,
) -> None:
    pickle.dump(
        obj,
        fhandle,
        protocol=protocol,
        fix_imports=False,
    )


def pickle_load(
    flike: str | bytes | PathLike[str] | BinaryIO | OpenFile | Path,
    *,
    use_dill: bool = False,
    compression: Optional[str] = None,
    filesystem: Optional[AbstractFileSystem] = None,
) -> object:
    load = __dill_load if use_dill else __pickle_load
    if filesystem is not None:
        with filesystem.open(
            flike,
            mode="rb",
            compression=compression,
        ) as f:
            return load(cast(BinaryIO, f))
    if isinstance(flike, (str, bytes, PathLike, Path)):
        with fsspec.open(
            flike,
            mode="rb",
            compression=compression,
        ) as f:
            return load(cast(BinaryIO, f))
    if isinstance(flike, OpenFile):
        return load(cast(BinaryIO, flike))
    return load(flike)


def pickle_dump(
    obj: object,
    flike: str | bytes | PathLike[str] | BinaryIO | OpenFile | Path,
    *,
    protocol: int = 5,
    use_dill: bool = False,
    compression: Optional[str] = None,
    filesystem: Optional[AbstractFileSystem] = None,
) -> None:
    dump = __dill_dump if use_dill else __pickle_dump
    if filesystem is not None:
        with filesystem.open(flike, mode="wb", compression=compression) as f:
            dump(obj, cast(BinaryIO, f), protocol)
            return
    if isinstance(flike, (str, bytes, PathLike, Path)):
        with fsspec.open(flike, mode="wb", compression=compression) as f:
            dump(obj, cast(BinaryIO, f), protocol)
            return
    if isinstance(flike, OpenFile):
        dump(obj, cast(BinaryIO, flike), protocol)
        return
    dump(obj, flike, protocol)


def dill_load(
    flike: str | bytes | PathLike[str] | BinaryIO | OpenFile | Path,
    *,
    compression: Optional[str] = None,
    filesystem: Optional[AbstractFileSystem] = None,
) -> object:
    load = __dill_load
    if filesystem is not None:
        with filesystem.open(
            flike,
            mode="rb",
            compression=compression,
        ) as f:
            return load(cast(BinaryIO, f))
    if isinstance(flike, (str, bytes, PathLike, Path)):
        with fsspec.open(
            flike,
            mode="rb",
            compression=compression,
        ) as f:
            return load(cast(BinaryIO, f))
    if isinstance(flike, OpenFile):
        return load(cast(BinaryIO, flike))
    return load(flike)


def dill_dump(
    obj: object,
    flike: str | bytes | PathLike[str] | BinaryIO | OpenFile | Path,
    *,
    protocol: int = 5,
    compression: Optional[str] = None,
    filesystem: Optional[AbstractFileSystem] = None,
) -> None:
    dump = __dill_dump
    if filesystem is not None:
        with filesystem.open(flike, mode="wb", compression=compression) as f:
            dump(obj, cast(BinaryIO, f), protocol)
            return
    if isinstance(flike, (str, bytes, PathLike, Path)):
        with fsspec.open(flike, mode="wb", compression=compression) as f:
            dump(obj, cast(BinaryIO, f), protocol)
            return
    if isinstance(flike, OpenFile):
        dump(obj, cast(BinaryIO, flike), protocol)
        return
    dump(obj, flike, protocol)
