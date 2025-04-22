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
from typing import TextIO, final, override

from unirule.exporter import BaseExporter

# All type checks have been done when importing. We can write as-is.


@final
class SingboxExporter(BaseExporter):
    @override
    def export(self, stream: TextIO) -> None:
        srs = {"version": 3, "rules": self.ir}
        json.dump(srs, stream)
