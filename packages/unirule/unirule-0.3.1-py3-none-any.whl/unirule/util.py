# Copyright (C) 2024 TargetLocked
#
# This file is part of unirule.
#
# unirule is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# unirule is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with unirule.  If not, see <https://www.gnu.org/licenses/>.


import io
import sys
from dataclasses import dataclass
from typing import TYPE_CHECKING, Callable, Optional, TextIO

from unirule.exception import IncapableInputError, IncapableOutputError

if TYPE_CHECKING:
    from unirule.exporter import BaseExporter
    from unirule.importer.adguarddns import AdguardDnsImporter


class Registry:
    """Registry for dispatching key to the corresponding hook function."""

    NOMATCH_CURRIED = "__nomatch_curried__"

    def __init__(self) -> None:
        self._data = {}
        self._nomatch_curried: Optional[Callable] = None

    def set(self, key: str, value: Callable) -> None:
        if key is self.NOMATCH_CURRIED:
            self._nomatch_curried = value
        elif key in self._data:
            raise ValueError(f"duplicate key in Registry: {key}")
        self._data[key] = value

    def get(self, key: str) -> Callable:
        try:
            return self._data[key]
        except KeyError:
            if self._nomatch_curried is not None:
                return self._nomatch_curried(key)
            raise ValueError(f"unsupported key: {key}") from None

    def key_handler(self, key: str) -> Callable:
        """Set the decorated function as a hook.

        Arguments:
            key -- key to use

        Returns:
            A decorator.
        """

        def _decorator(func: Callable) -> Callable:
            self.set(key, func)
            return func

        return _decorator


@dataclass
class _GlobalMap:
    pedantic: bool = False


uglobal = _GlobalMap()


def minify_rule(rule: dict) -> dict:
    new_rule = rule.copy()
    for key, value in rule.items():
        if len(value) == 0:
            del new_rule[key]
    return new_rule


def info(info: str) -> None:
    print(f"[INFO] {info}", file=sys.stderr)


def warn(info: str) -> None:
    print(f"[WARN] {info}", file=sys.stderr)


def error(info: str) -> None:
    print(f"[ERROR] {info}", file=sys.stderr)


def incapable_input(reason: str) -> None:
    if uglobal.pedantic:
        raise IncapableInputError(reason)
    else:
        warn(reason)


def incapable_output(reason: str) -> None:
    if uglobal.pedantic:
        raise IncapableOutputError(reason)
    else:
        warn(reason)


def unreachable() -> None:
    raise RuntimeError("internal error")


def create_istream(path: str) -> TextIO:
    if path == "stdin":
        return sys.stdin
    return io.TextIOWrapper(
        io.BufferedReader(io.FileIO(path, mode="r")), encoding="utf-8"
    )


def create_ostream(path: str) -> TextIO:
    if path == "stdout":
        return sys.stdout
    return io.TextIOWrapper(
        io.BufferedWriter(io.FileIO(path, mode="w")), encoding="utf-8", newline="\n"
    )


def _minify_expr(lhs: str, op: str, rhs: str) -> str:
    if len(lhs) == 0:
        return rhs
    if len(rhs) == 0:
        return lhs
    return f"({lhs} {op} {rhs})"


def multiple_output_from_adg(
    importer: "AdguardDnsImporter", exporter: "BaseExporter", output_tmpl: str
) -> None:
    if output_tmpl.count("{}") != 1:
        raise ValueError('output-path must contain one "{}" as placeholder')
    # ((normal_rule && !normal_exception) || important_rule) && !important_exception
    adgresult = importer.adg_result
    i = 0
    expr = ""
    for name_tmpl, rule, op in [
        ("item_{}", adgresult.normal_rule, ""),
        ("!item_{}", adgresult.normal_exception, "&&"),
        ("item_{}", adgresult.important_rule, "||"),
        ("!item_{}", adgresult.important_exception, "&&"),
    ]:
        if len(rule) == 0:
            continue
        expr = _minify_expr(expr, op, name_tmpl.format(i))
        output_path = output_tmpl.format(i)
        i += 1
        exporter.set_ir([rule])
        exporter.export(create_ostream(output_path))
    info(f"multiple output: total items: {i}")
    info(f"multiple output: equivalent expression: {expr}")
