# coding=utf-8
import argparse


class ArgsNamespace(argparse.Namespace):
    potater: bool
    glsl: bool
    properties: bool
    block: bool
    item: bool
    entity: bool
    output: str
    input: str
    print_args: bool
    skip_processing_output_print: bool
    skip_processing_type_print: bool
