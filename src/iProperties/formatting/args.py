# coding=utf-8
import argparse


class ArgsNamespace(argparse.Namespace):
    potater: bool
    glsl: bool
    properties: bool

    block: bool
    item: bool
    entity: bool

    input: str
    output: str
    properties_output: str | None
    glsl_output: str | None
    potater_output: str | None

    print_args: bool
    skip_processing_output_print: bool
    skip_processing_type_print: bool
