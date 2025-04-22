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

from typing import Callable, TextIO, final, override

from unirule.exception import BadIrError
from unirule.exporter import BaseExporter
from unirule.util import Registry, incapable_output

# for key
_reg = Registry()


@_reg.key_handler("domain")
def _trans_domain(value: list[str]) -> list[str]:
    # Match full domain.
    return [f"full:{item}" for item in value]


@_reg.key_handler("domain_suffix")
def _trans_domain_suffix(value: list[str]) -> list[str]:
    # Match domain suffix.
    # FIXME: items prefixed with '.' should be literal suffix
    return [f"{item.removeprefix('.')}" for item in value]


@_reg.key_handler("domain_keyword")
def _trans_domain_keyword(value: list[str]) -> list[str]:
    # Match domain using keyword.
    return [f"keyword:{item}" for item in value]


@_reg.key_handler("domain_regex")
def _trans_domain_regex(value: list[str]) -> list[str]:
    # Match domain using regular expression.
    return [f"regexp:{item}" for item in value]


@_reg.key_handler(Registry.NOMATCH_CURRIED)
def _unknown_field(key: str) -> Callable:
    def _trans_unknown(_) -> list[str]:
        return []

    incapable_output(f"unsupported IR field: {key}")
    return _trans_unknown


# 1 rule item -> N rule lines
def _export_dlc(rule: dict) -> list[str]:
    results = []
    match tp := rule.get("type"):
        case None:
            for key, value in rule.items():
                if len(value) == 0:
                    continue
                # translate all fields
                trans_func = _reg.get(key)
                results.extend(trans_func(value))
        case "logical":
            incapable_output("logical rule is not supported")
        case _:
            raise BadIrError(f"unexpected rule type: {tp}")
    return results


@final
class DlcExporter(BaseExporter):
    @override
    def export(self, stream: TextIO) -> None:
        rules = []
        for item in self.ir:
            rules.extend(_export_dlc(item))
        stream.write("\n".join(rules))
