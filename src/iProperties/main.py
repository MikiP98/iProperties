# coding=utf-8
import argparse
import os
from typing import cast

import iProperties.preprocessor as preprocessor
from iProperties.formatting import ArgsNamespace, bold, gray, green, it, red, reset

__version__ = '1.1.0'


def main() -> None:
    print(f"{bold}{green}iProperties! {__version__}{reset}")

    args = parse_arguments()
    if args.print_args:
        print(f"{args=}")

    if not args.skip_processing_output_print:
        print(f"{it}{gray}- PoTater: {args.potater}{reset}")
        print(f"{it}{gray}- GLSL: {args.glsl}{reset}")
        print(f"{it}{gray}- Properties: {args.properties}{reset}")
    if not args.skip_processing_type_print:
        print(f"{it}{gray}- Block: {args.block}{reset}")
        print(f"{it}{gray}- Item: {args.item}{reset}")
        print(f"{it}{gray}- Entity: {args.entity}{reset}")
    if not (args.skip_processing_output_print or args.skip_processing_type_print):
        print()

    preprocessor.compile_properties(args)


def parse_arguments() -> ArgsNamespace:
    # Parse flags

    # --potater    -po (T/F) -> should the PoTater conversion be saved (default: false)
    # --glsl       -g  (T/F) -> should the GLSL be saved (default: true)
    # --properties -pr (T/F) -> should the properties be saved (default: true)

    # --block  -b (T/F) -> should the block properties template be processed (default: true)
    # --item   -it (T/F) -> should the item properties template be processed (default: true)
    # --entity -e (T/F) -> should the entity properties template be processed (default: true)

    # --input  -in (str) -> input directory (default: active directory './')
    # --output -o (str) -> output directory (default: active directory './')
    # --properties-output -pro (str) -> override output directory for the property files (default: None)
    # --glsl-output -gl (str) -> override output directory for the glsl define files (default: None)
    # --potater-output -po (str) -> override output directory for the PoTater conversion (default: None)

    # DEBUG
    # --print-args (T/F) -> print the parsed arguments
    # --skip-processing-output-print -> skip printing which files will be outputted
    # --skip-processing-type-print -> skip printing the processing type

    parser = argparse.ArgumentParser(
        description="Process and save various data templates with configurable options."
    )

    # Boolean flags using BooleanOptionalAction
    parser.add_argument("--potater", "-po", action=argparse.BooleanOptionalAction, default=False,
                        help="Save the PoTater conversion (default: false)")
    parser.add_argument("--glsl", "-g", action=argparse.BooleanOptionalAction, default=True,
                        help="Save the GLSL (default: true)")
    parser.add_argument("--properties", "-pr", action=argparse.BooleanOptionalAction, default=True,
                        help="Save the properties (default: true)")

    # Boolean options using BooleanOptionalAction
    parser.add_argument("--block", "-b", action=argparse.BooleanOptionalAction, default=True,
                        help="Process the block properties template (default: true)")
    parser.add_argument("--item", "-it", action=argparse.BooleanOptionalAction, default=True,
                        help="Process the item properties template (default: true)")
    parser.add_argument("--entity", "-e", action=argparse.BooleanOptionalAction, default=True,
                        help="Process the entity properties template (default: true)")

    # String arguments
    parser.add_argument("--input", "-in", type=str, default="./",
                        help="Input directory (default: './')")
    parser.add_argument("--output", "-o", type=str, default="./",
                        help="Output directory (default: './')")

    parser.add_argument("--properties-output", "-pro", type=str, default=None,
                        help="Override output directory for the property files (default: None)")
    parser.add_argument("--glsl-output", "-go", type=str, default=None,
                        help="Override output directory for the GLSL define files (default: None)")
    parser.add_argument("--potater-output", "-pot", type=str, default=None,
                        help="Override output directory for the PoTater conversion (default: None)")

    # DEBUG
    parser.add_argument("--print-args", "-pa", action=argparse.BooleanOptionalAction, default=False,
                        help="Print the parsed arguments (default: false)")
    parser.add_argument("--skip-processing-output-print", "-spo", action="store_true", default=False,
                        help="Skip printing which files will be outputted")
    parser.add_argument("--skip-processing-type-print", "-spt", action="store_true", default=False,
                        help="Skip printing the processing type")

    args = cast(ArgsNamespace, parser.parse_args())

    # make sure the folder paths end with '/'
    if not (args.input[-1] == '/' or args.input[-1] == '\\' or args.input[-1] == ''):
        print(f"{red}Incorrect input folder path;{reset} {it}changing '{args.input}' to '{args.input + '/'}'{reset}")
        args.input += '/'

    if not (args.output[-1] == '/' or args.output[-1] == '\\' or args.output[-1] == ''):
        print(f"{red}Incorrect output folder path;{reset} {it}changing '{args.output}' to '{args.output + '/'}'{reset}")
        args.output += '/'

    if not (args.properties_output is None or args.properties_output[-1] == '/' or args.properties_output[-1] == '\\' or args.properties_output[-1] == ''):
        print(f"{red}Incorrect properties output folder path;{reset} {it}changing '{args.properties_output}' to '{args.properties_output + '/'}'{reset}")
        args.properties_output += '/'
    if not (args.glsl_output is None or args.glsl_output[-1] == '/' or args.glsl_output[-1] == '\\' or args.glsl_output[-1] == ''):
        print(f"{red}Incorrect glsl output folder path;{reset} {it}changing '{args.glsl_output}' to '{args.glsl_output + '/'}'{reset}")
        args.glsl_output += '/'
    if not (args.potater_output is None or args.potater_output[-1] == '/' or args.potater_output[-1] == '\\' or args.potater_output[-1] == ''):
        print(f"{red}Incorrect potater output folder path;{reset} {it}changing '{args.potater_output}' to '{args.potater_output + '/'}'{reset}")
        args.potater_output += '/'

    # If output path does not exist, create it
    if not os.path.exists(args.output):
        print(f"{it}Creating output folder '{args.output}'{reset}")
        os.makedirs(args.output)
    if args.properties_output is not None and not os.path.exists(args.properties_output):
        print(f"{it}Creating properties output folder '{args.properties_output}'{reset}")
        os.makedirs(args.properties_output)
    if args.glsl_output is not None and not os.path.exists(args.glsl_output):
        print(f"{it}Creating glsl output folder '{args.glsl_output}'{reset}")
        os.makedirs(args.glsl_output)
    if args.potater_output is not None and not os.path.exists(args.potater_output):
        print(f"{it}Creating potater output folder '{args.potater_output}'{reset}")
        os.makedirs(args.potater_output)

    return args


if __name__ == '__main__':
    main()
