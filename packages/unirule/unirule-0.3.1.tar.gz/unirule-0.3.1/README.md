# unirule

Rule converter for proxy platforms.

unirule supports rules in text formats only. For binary formats, we recommend [MetaCubeX/geo](https://github.com/MetaCubeX/geo).

## Install

unirule requires Python >= 3.10 .

```bash
pip install unirule
```

## Usage

```bash
unirule -h
```

```plain
usage: unirule [-h] -i {singbox,dlc,meta-domain-yaml,meta-domain-text,meta-ipcidr-yaml,meta-ipcidr-text,adguard-dns,adguard-dns-multiout} -o
               {singbox,dlc,meta-domain-yaml,meta-domain-text,meta-ipcidr-yaml,meta-ipcidr-text} [-p]
               input_path output_path

positional arguments:
  input_path            "stdin" or path to the input file
  output_path           "stdout" or path to the output file

options:
  -h, --help            show this help message and exit
  -i {singbox,dlc,meta-domain-yaml,meta-domain-text,meta-ipcidr-yaml,meta-ipcidr-text,adguard-dns,adguard-dns-multiout}, --input-type {singbox,dlc,meta-domain-yaml,meta-domain-text,meta-ipcidr-yaml,meta-ipcidr-text,adguard-dns,adguard-dns-multiout}
                        type of the input file
  -o {singbox,dlc,meta-domain-yaml,meta-domain-text,meta-ipcidr-yaml,meta-ipcidr-text}, --output-type {singbox,dlc,meta-domain-yaml,meta-domain-text,meta-ipcidr-yaml,meta-ipcidr-text}
                        type of the output file
  -p, --pedantic        mark all warnings as errors
```

## Develop

This project uses [Rye](https://rye.astral.sh/).

```bash
git clone https://github.com/TargetLocked/unirule.git
cd unirule
rye sync
```
