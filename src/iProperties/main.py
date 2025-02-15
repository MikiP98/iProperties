# coding=utf-8
import argparse
import os
from typing import cast

import iProperties.preprocessor as preprocessor
from iProperties.formatting import ArgsNamespace, bold, gray, green, it, red, reset

__version__ = '1.0.1'


def main() -> None:
    print(f"{bold}{green}iProperties! {__version__}{reset}")

    args = parse_arguments()
    if args.print_args:
        print(f"{args=}")

    if not args.skip_processing_output_print:
        print(f"{it}{gray}- PoTaTer: {args.potater}{reset}")
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

    # --potater    -po (T/F) -> should the PoTaTer conversion be saved (default: false)
    # --glsl       -g  (T/F) -> should the GLSL be saved (default: true)
    # --properties -pr (T/F) -> should the properties be saved (default: true)

    # --block  -b (T/F) -> should the block properties template be processed (default: true)
    # --item   -it (T/F) -> should the item properties template be processed (default: true)
    # --entity -e (T/F) -> should the entity properties template be processed (default: true)

    # --output -o (str) -> output directory (default: active directory './')
    # --input  -in (str) -> input directory (default: active directory './')

    # DEBUG
    # --print-args (T/F) -> print the parsed arguments
    # --skip-processing-output-print -> skip printing the output directory
    # --skip-processing-type-print -> skip printing the processing type

    parser = argparse.ArgumentParser(
        description="Process and save various data templates with configurable options."
    )

    # Boolean flags using BooleanOptionalAction
    parser.add_argument("--potater", "-po", action=argparse.BooleanOptionalAction, default=False,
                        help="Save the PoTaTer conversion (default: false)")
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
    parser.add_argument("--output", "-o", type=str, default="./",
                        help="Output directory (default: './')")
    parser.add_argument("--input", "-in", type=str, default="./",
                        help="Input directory (default: './')")

    # DEBUG
    parser.add_argument("--print-args", "-pa", action=argparse.BooleanOptionalAction, default=False,
                        help="Print the parsed arguments (default: false)")
    parser.add_argument("--skip-processing-output-print", "-spo", action="store_true", default=False,
                        help="Skip printing the output directory")
    parser.add_argument("--skip-processing-type-print", "-spt", action="store_true", default=False,
                        help="Skip printing the processing type")

    args = cast(ArgsNamespace, parser.parse_args())

    # make sure the folder paths end with '/'
    if not (args.output[-1] == '/' or args.output[-1] == '\\' or args.output[-1] == ''):
        print(f"{red}Incorrect output folder path;{reset} {it}changing '{args.output}' to '{args.output + '/'}'{reset}")
        args.output += '/'

    # make sure the folder paths end with '/'
    if not (args.input[-1] == '/' or args.input[-1] == '\\' or args.input[-1] == ''):
        print(f"{red}Incorrect input folder path;{reset} {it}changing '{args.input}' to '{args.input + '/'}'{reset}")
        args.input += '/'

    # If output path does not exist, create it
    if not os.path.exists(args.output):
        print(f"{it}Creating output folder '{args.output}'{reset}")
        os.makedirs(args.output)

    return args


if __name__ == '__main__':
    main()
