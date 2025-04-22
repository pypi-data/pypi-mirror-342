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

import json
from typing import Any, TextIO, final, override

from unirule.exception import InvalidInputError
from unirule.importer import BaseImporter
from unirule.util import Registry, minify_rule

# The format is almost identical to the IR, except for Listable items
# where using a list is mandatory even if there is only one item.
# Here we only wrap the single items and check types.

# for key
_reg = Registry()


@_reg.key_handler("network")
@_reg.key_handler("domain")
@_reg.key_handler("domain_suffix")
@_reg.key_handler("domain_keyword")
@_reg.key_handler("domain_regex")
@_reg.key_handler("source_ip_cidr")
@_reg.key_handler("ip_cidr")
@_reg.key_handler("source_port_range")
@_reg.key_handler("port_range")
@_reg.key_handler("process_name")
@_reg.key_handler("process_path")
@_reg.key_handler("package_name")
@_reg.key_handler("wifi_ssid")
@_reg.key_handler("wifi_bssid")
def _fmt_str(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    elif isinstance(value, list):
        for item in value:
            if not isinstance(item, str):
                raise InvalidInputError(
                    f"unexpected value type: {item} should be typed str"
                )
        return value
    else:
        raise InvalidInputError(f"unexpected value type: {value} should be typed str")


@_reg.key_handler("source_port")
@_reg.key_handler("port")
def _fmt_int(value: Any) -> list[int]:
    if isinstance(value, int):
        return [value]
    elif isinstance(value, list):
        for item in value:
            if not isinstance(item, int):
                raise InvalidInputError(
                    f"unexpected value type: {item} should be typed int"
                )
        return value
    else:
        raise InvalidInputError(f"unexpected value type: {value} should be typed int")


@_reg.key_handler("query_type")
def _fmt_str_or_int(value: Any) -> list[str | int]:
    if isinstance(value, (str, int)):
        return [value]
    elif isinstance(value, list):
        for item in value:
            if not isinstance(item, (str, int)):
                raise InvalidInputError(
                    f"unexpected value type: {item} should be typed str or int"
                )
        return value
    else:
        raise InvalidInputError(
            f"unexpected value type: {value} should be typed str or int"
        )


@_reg.key_handler("invert")
def _fmt_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    else:
        raise InvalidInputError(f"unexpected value type: {value} should be typed bool")


# 1 rule item -> 1 rule item
def _import_singbox(rule: dict) -> dict:
    match tp := rule.get("type"):
        case None:
            for key, value in rule.items():
                # format all fields
                fmt = _reg.get(key)
                rule[key] = fmt(value)
        case "logical":
            for key, value in rule.items():
                match key:
                    case "type":
                        pass
                    case "mode":
                        if value not in ("and", "or"):
                            raise InvalidInputError(
                                f'unsupported logical mode: {rule["mode"]}'
                            )
                    case "invert":
                        _fmt_bool(value)
                    case _:
                        raise InvalidInputError(f"unsupported logical field: {key}")
            # parse all sub-rules
            rule["rules"] = [_import_singbox(subrule) for subrule in rule["rules"]]
        case _:
            raise InvalidInputError(f"unsupported rule type: {tp}")
    return minify_rule(rule)


@final
class SingboxImporter(BaseImporter):
    @override
    def import_(self, stream: TextIO) -> None:
        content = json.load(stream)
        # source format: { "version": 0, "rules": [] }
        self.ir = [_import_singbox(rule) for rule in content["rules"]]
