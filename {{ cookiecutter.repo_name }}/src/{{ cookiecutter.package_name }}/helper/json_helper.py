from os import PathLike
from pathlib import Path
from typing import cast
from typing import Optional
from typing import TextIO
from typing import Type
from typing import TypeAlias

import fsspec
import ujson
from fsspec.core import OpenFile
from fsspec.spec import AbstractFileSystem

JSONType: TypeAlias = dict[str, "JSONType"] | list["JSONType"] | int | str | float | bool | Type[None]


def json_load(
    flike: str | Path | PathLike[str] | TextIO | OpenFile,
    *,
    compression: Optional[str] = None,
    filesystem: Optional[AbstractFileSystem] = None,
) -> JSONType:
    if filesystem is not None:
        with filesystem.open(
            flike,
            mode="rt",
            encoding="utf-8",
            compression=compression,
        ) as f:
            return cast(JSONType, ujson.load(cast(TextIO, f)))
    if isinstance(flike, (str, PathLike, Path)):
        with fsspec.open(
            flike,
            mode="rt",
            encoding="utf-8",
            compression=compression,
        ) as f:
            return cast(JSONType, ujson.load(cast(TextIO, f)))
    if isinstance(flike, OpenFile):
        return cast(JSONType, ujson.load(cast(TextIO, flike)))
    return cast(JSONType, ujson.load(flike))


def json_dump(
    obj: JSONType,
    flike: str | Path | PathLike[str] | TextIO | OpenFile,
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

    if filesystem is not None:
        with filesystem.open(flike, mode="wt", encoding="utf-8", compression=compression) as f:
            do_dump(cast(TextIO, f))
            return
    if isinstance(flike, (str, PathLike, Path)):
        with fsspec.open(flike, mode="wt", encoding="utf-8", compression=compression) as f:
            do_dump(cast(TextIO, f))
            return
    if isinstance(flike, OpenFile):
        do_dump(cast(TextIO, flike))
        return
    do_dump(flike)
