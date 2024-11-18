# coding=utf-8
import iProperties.compiler as compiler

__version__ = '0.0.1'


def main_cli():
    main(flags_required=False)


def main(flags_required=True):
    print(f'Hello PyCharm! {__version__}')
    # Parse flags

    # If flags are missing and `flags_required` is True, ask for input

    compiler.compile_properties()


if __name__ == '__main__':
    main(flags_required=True)
