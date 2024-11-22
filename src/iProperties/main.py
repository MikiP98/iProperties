# coding=utf-8
import iProperties.preprocessor as preprocessor

__version__ = '0.0.1'


def main_cli():
    main(flags_required=False)


def main():
    print(f'Hello PyCharm! {__version__}')
    # Parse flags

    preprocessor.compile_properties()


if __name__ == '__main__':
    main()
