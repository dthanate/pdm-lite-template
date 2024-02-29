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
    encoding: str = "utf-8",
    compression: Optional[str] = None,
    filesystem: Optional[AbstractFileSystem] = None,
) -> JSONType:
    """Load a json object from a file or a fsspec url path into a python dictionary (using ujson).

    Args:
        encoding: The encoding to use.
        compression: None, "infer", or a name of a compresion scheme (see fsspec.available_compression()).
        filesystem: fsspec filesystem to use, not needed for a local file.

    Returns:
        A python dictionary.
    """
    if isinstance(flike, (str, PathLike, Path)):
        if filesystem is not None:
            with filesystem.open(
                flike,
                mode="rt",
                encoding=encoding,
                compression=compression,
            ) as f:
                return cast(JSONType, ujson.load(cast(IOBase, f)))
        with fsspec.open(
            flike,
            mode="rt",
            encoding=encoding,
            compression=compression,
        ) as f:
            return cast(JSONType, ujson.load(cast(IOBase, f)))
    return cast(JSONType, ujson.load(flike))


def json5_load(
    flike: str | Path | PathLike[str] | TextIO,
    /,
    *,
    encoding: str = "utf-8",
    compression: Optional[str] = None,
    filesystem: Optional[AbstractFileSystem] = None,
) -> JSONType:
    """Load a json5 object from a file or a fsspec url path into a python dictionary (using pyjson5).

    Args:
        encoding: The encoding to use.
        compression: None, "infer", or a name of a compresion scheme (see fsspec.available_compression()).
        filesystem: fsspec filesystem to use.

    Returns:
        A python dictionary.
    """
    if isinstance(flike, (str, PathLike, Path)):
        if filesystem is not None:
            with filesystem.open(
                flike,
                mode="rt",
                encoding=encoding,
                compression=compression,
            ) as f:
                return cast(JSONType, pyjson5.decode_io(cast(IOBase, f)))
        with fsspec.open(
            flike,
            mode="rt",
            encoding=encoding,
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
    escape_forward_slash: bool = False,
    encode_html_chars: bool = False,
    compression: Optional[str] = None,
    filesystem: Optional[AbstractFileSystem] = None,
) -> None:
    """Dump a correctly typed python dictionary into a json file or a fsspec url path (using ujson).

    Args:
        indent: Amount of indentation (pretty printing).
        ensure_ascii: Use escape code for non-ASCII characters.
        escape_forward_slash: Whether forward slashes are escaped.
        encode_html_chars: Encode unsafe HTML characters.
        compression: None, "infer", or a name of a compresion scheme (see fsspec.available_compression()).
        filesystem: fsspec filesystem to use.

    Returns:
        Nothing
    """

    def do_dump(f: TextIO) -> None:
        ujson.dump(
            obj,
            f,
            indent=indent,
            ensure_ascii=ensure_ascii,
            escape_forward_slashes=escape_forward_slash,
            encode_html_chars=encode_html_chars,
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
