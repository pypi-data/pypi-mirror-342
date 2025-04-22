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

import argparse

from unirule.exporter.dlc import DlcExporter
from unirule.exporter.metadomain import MetaDomainTextExporter, MetaDomainYamlExporter
from unirule.exporter.metaipcidr import MetaIpcidrTextExporter, MetaIpcidrYamlExporter
from unirule.exporter.singbox import SingboxExporter
from unirule.importer.adguarddns import AdguardDnsImporter
from unirule.importer.dlc import DlcImporter
from unirule.importer.metadomain import MetaDomainTextImporter, MetaDomainYamlImporter
from unirule.importer.metaipcidr import MetaIpcidrTextImporter, MetaIpcidrYamlImporter
from unirule.importer.singbox import SingboxImporter
from unirule.util import (
    create_istream,
    create_ostream,
    multiple_output_from_adg,
    uglobal,
)

INPUT_TYPES = {
    "singbox": SingboxImporter,
    "dlc": DlcImporter,
    "meta-domain-yaml": MetaDomainYamlImporter,
    "meta-domain-text": MetaDomainTextImporter,
    "meta-ipcidr-yaml": MetaIpcidrYamlImporter,
    "meta-ipcidr-text": MetaIpcidrTextImporter,
    "adguard-dns": AdguardDnsImporter,
    "adguard-dns-multiout": AdguardDnsImporter,
}

OUTPUT_TYPES = {
    "singbox": SingboxExporter,
    "dlc": DlcExporter,
    "meta-domain-yaml": MetaDomainYamlExporter,
    "meta-domain-text": MetaDomainTextExporter,
    "meta-ipcidr-yaml": MetaIpcidrYamlExporter,
    "meta-ipcidr-text": MetaIpcidrTextExporter,
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", help='"stdin" or path to the input file')
    parser.add_argument("output_path", help='"stdout" or path to the output file')
    parser.add_argument(
        "-i",
        "--input-type",
        help="type of the input file",
        required=True,
        choices=INPUT_TYPES.keys(),
    )
    parser.add_argument(
        "-o",
        "--output-type",
        help="type of the output file",
        required=True,
        choices=OUTPUT_TYPES.keys(),
    )
    parser.add_argument(
        "-p", "--pedantic", help="mark all warnings as errors", action="store_true"
    )

    args = parser.parse_args()

    uglobal.pedantic = args.pedantic

    # find importer and exporter
    importer = INPUT_TYPES[args.input_type]()
    exporter = OUTPUT_TYPES[args.output_type]()

    importer.import_(create_istream(args.input_path))
    if args.input_type == "adguard-dns-multiout":
        multiple_output_from_adg(importer, exporter, args.output_path)
    else:
        exporter.set_ir(importer.get_ir())
        exporter.export(create_ostream(args.output_path))

    return 0
