from io import IOBase
from os import PathLike
from pathlib import Path
from typing import cast
from typing import Optional
from typing import TextIO
from typing import TypeAlias

import fsspec
import pyjson5
import ujson
from fsspec.spec import AbstractFileSystem

JSONType: TypeAlias = dict[str, "JSONType"] | list["JSONType"] | int | str | float | bool | None


def json_load(
    flike: str | Path | PathLike[str] | TextIO,
    /,
    *,
    compression: Optional[str] = None,
    filesystem: Optional[AbstractFileSystem] = None,
) -> JSONType:
    if isinstance(flike, (str, PathLike, Path)):
        if filesystem is not None:
            with filesystem.open(
                flike,
                mode="rt",
                encoding="utf-8",
                compression=compression,
            ) as f:
                return cast(JSONType, ujson.load(cast(IOBase, f)))
        with fsspec.open(
            flike,
            mode="rt",
            encoding="utf-8",
            compression=compression,
        ) as f:
            return cast(JSONType, ujson.load(cast(IOBase, f)))
    return cast(JSONType, ujson.load(flike))


def json5_load(
    flike: str | Path | PathLike[str] | TextIO,
    /,
    *,
    compression: Optional[str] = None,
    filesystem: Optional[AbstractFileSystem] = None,
) -> JSONType:
    if isinstance(flike, (str, PathLike, Path)):
        if filesystem is not None:
            with filesystem.open(
                flike,
                mode="rt",
                encoding="utf-8",
                compression=compression,
            ) as f:
                return cast(JSONType, pyjson5.decode_io(cast(IOBase, f)))
        with fsspec.open(
            flike,
            mode="rt",
            encoding="utf-8",
            compression=compression,
        ) as f:
            return cast(JSONType, pyjson5.decode_io(cast(IOBase, f)))
    return cast(JSONType, pyjson5.decode_io(cast(IOBase, flike)))


def json_dump(
    obj: JSONType,
    flike: str | Path | PathLike[str] | TextIO,
    /,
    *,
    indent: int = 0,
    ensure_ascii: bool = False,
    compression: Optional[str] = None,
    filesystem: Optional[AbstractFileSystem] = None,
) -> None:
    def do_dump(f: TextIO) -> None:
        ujson.dump(
            obj,
            f,
            indent=indent,
            ensure_ascii=ensure_ascii,
        )

    if isinstance(flike, (str, PathLike, Path)):
        if filesystem is not None:
            with filesystem.open(flike, mode="wt", encoding="utf-8", compression=compression) as f:
                do_dump(cast(TextIO, f))
                return
        with fsspec.open(flike, mode="wt", encoding="utf-8", compression=compression) as f:
            do_dump(cast(TextIO, f))
            return
    do_dump(flike)
