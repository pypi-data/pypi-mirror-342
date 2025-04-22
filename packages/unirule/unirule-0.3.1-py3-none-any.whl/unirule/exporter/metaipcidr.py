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

import yaml

from unirule.exception import BadIrError
from unirule.exporter import BaseExporter
from unirule.util import Registry, incapable_output

# for key
_reg = Registry()


@_reg.key_handler("ip_cidr")
def _trans_ipcidr(value: list[str]) -> list[str]:
    return value


@_reg.key_handler(Registry.NOMATCH_CURRIED)
def _unknown_field(key: str) -> Callable:
    def _trans_unknown(_) -> list[str]:
        return []

    incapable_output(f"unsupported IR field: {key}")
    return _trans_unknown


# 1 rule item -> N rule lines
def _export_metaipcidr(rule: dict) -> list[str]:
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
class MetaIpcidrYamlExporter(BaseExporter):
    @override
    def export(self, stream: TextIO) -> None:
        rules = []
        for item in self.ir:
            rules.extend(_export_metaipcidr(item))
        # format: { payload: [] }
        yaml.dump({"payload": rules}, stream)


@final
class MetaIpcidrTextExporter(BaseExporter):
    @override
    def export(self, stream: TextIO) -> None:
        rules = []
        for item in self.ir:
            rules.extend(_export_metaipcidr(item))
        stream.write("\n".join(rules))
