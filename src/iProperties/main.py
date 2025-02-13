# coding=utf-8
import iProperties.preprocessor as preprocessor

__version__ = '0.2.1'


def main_cli():
    main()


def main():
    print(f'iProperties! {__version__}')
    # Parse flags

    preprocessor.compile_properties()


if __name__ == '__main__':
    main()
