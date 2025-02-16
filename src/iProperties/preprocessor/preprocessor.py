# coding=utf-8
import os

from enum import auto, IntEnum
from typing import Callable, Self, TextIO

from iProperties.formatting import ArgsNamespace, blue, bold, it, red, reset, yellow


class LineType(IntEnum):
    COMMENT = auto()
    DEFINE_COMMENT = auto()
    IPROPERTY_COMMENT = auto()
    GLSL_COMMENT = auto()
    VARIABLE = auto()
    PROPERTY_DECLARATION = auto()
    EMPTY_LINE = auto()
    OTHER = auto()


class Preprocessor:
    def __init__(self, file: TextIO):
        self.file = file

        self.compiled_properties: list[str] = []
        self.compiled_glsl: list[str] = []

        self.potater: list[str] = []
        self.potater_variable_line_splittings: dict[str, list[str]] = {}

        self.variables: dict[str, list[str]] = {}
        self.current_glsl_key = "NONE"
        self.was_glsl_key_used = True

        self.used_numbers: list[int] = []
        self.directly_used_variables: list[str] = []  # if not in this list, don't copy to PoTater
        self.last_id: None | str = None

        line_nr = 0
        while line := file.readline():
            line_nr += 1
            line_type = self.determine_line_type(line)
            processing_method = self.line_processing_function[line_type]
            processing_method(self, line)

    def get_compiled_properties(self) -> str:
        property_id = 1
        last_id = None
        for i, value in enumerate(self.compiled_properties):
            if "block." in value or "item." in value or "entity." in value:
                key = value.split('=', 1)[0]
                str_property_id = key.split('.', 1)[1]
                if str_property_id.isdigit():
                    last_id = int(str_property_id)
                    property_id = last_id + 1

            while property_id in self.used_numbers:
                property_id += 1

            if '**' in value:
                value = value.replace('**', str(last_id))
            if '*' in value:
                value = value.replace('*', str(property_id))
                last_id = property_id
                property_id += 1

            self.compiled_properties[i] = value

        return '\n'.join(self.compiled_properties).strip()

    def get_compiled_glsl(self) -> str:
        id = 1
        for i, value in enumerate(self.compiled_glsl):
            if '*' not in value:
                str_property_id = value.split(' ', 2)[2]
                if str_property_id.isdigit():
                    id = int(str_property_id)

            while id in self.used_numbers:
                id += 1

            if '**' in value:
                value = value.replace('**', str(id - 1))

            if '*' in value:
                value = value.replace('*', str(id))
                id += 1

            self.compiled_glsl[i] = value

        return '\n'.join(self.compiled_glsl).strip()

    def get_potater(self) -> str:
        processed_potater = []

        for line in self.potater:
            processed_potater.append(line)

        return '\n'.join(processed_potater).strip()

    @staticmethod
    def determine_line_type(line: str) -> LineType:
        line = line.strip()
        if len(line) >= 1:
            if line[0] == '#':
                if len(line) == 1:
                    pass
                elif line[1] == '=':
                    return LineType.GLSL_COMMENT
                elif line[1] == '$':
                    return LineType.IPROPERTY_COMMENT
                elif len(line) >= 7:
                    if line[1:7].lower() == "define":
                        return LineType.DEFINE_COMMENT

                return LineType.COMMENT

            elif line[0] == '$':
                return LineType.VARIABLE
            else:
                # if line.strip()[:6] in frozenset(("block.", "item.", "entity.")):
                if any(x in line[:7] for x in ("block.", "item.", "entity.")):
                    return LineType.PROPERTY_DECLARATION
                else:
                    return LineType.OTHER
        else:
            return LineType.EMPTY_LINE

    def process_empty_line(self, line: str) -> None:
        self.compiled_properties.append(line.strip())
        self.potater.append(line.strip())

    def process_comment(self, line: str) -> None:
        self.compiled_properties.append(line.rstrip())
        self.potater.append(line.rstrip())

    def process_define_comment(self, line: str) -> None:
        line_content = line.strip()
        padding_length = len(line.rstrip()) - len(line_content)
        if padding_length == 0:
            padding = ""
        else:
            padding = line[:padding_length]

        define, key, values = line_content.split(' ', 2)

        variable_values = self.pre_process_values(values.split(' '))
        variable_values_string = ' '.join(variable_values)
        entry = f"{padding}#define {key} {variable_values_string}"

        self.compiled_properties.append(entry)
        self.potater.append(entry)

    def process_iproperty_comment(self, _: str) -> None:
        # Ignore/delete
        pass

    def process_glsl_comment(self, line: str) -> None:
        if not self.was_glsl_key_used:
            print(f"{yellow}WARNING: GLSL key: `{self.current_glsl_key}`, was never used{reset}")
        self.current_glsl_key = line.strip()[2:].strip()
        self.was_glsl_key_used = False

        self.potater.append(line.rstrip())

    def process_variable(self, line: str) -> None:
        line = line.strip()[1:]

        parts = line.split('=', 1)

        key = parts[0].strip()
        values = parts[1].strip().split(' ')

        self.variables[key] = self.pre_process_values(values, variable=True)

        if r"\n" not in self.variables[key]:
            # print(f"'\\n' not found in '{key}': {self.variables[key]}")
            self.potater.append(f"group.{key} = {' '.join(self.variables[key])}")
        else:
            # print(f"'\\n' found in '{key}': {self.variables[key]}")
            lines = ' '.join(self.variables[key]).split(r" \n ")
            self.potater_variable_line_splittings[key] = []
            for i, line in enumerate(lines):
                modId = line.split(':', 1)[0].strip()
                self.potater_variable_line_splittings[key].append(modId)
                entry = f"group.{key}_{modId} = {line}"
                self.potater.append(entry)
            # print(self.potater_variable_line_splittings)

    def process_property_declaration(self, line: str) -> None:
        line_content = line.strip()
        padding_length = len(line.rstrip()) - len(line_content)
        if padding_length == 0:
            padding = ""
        else:
            padding = line[:padding_length - 1]

        parts = line_content.split('=', 1)

        key = parts[0].strip()
        values = parts[1].strip().split(' ')

        id: str
        _, id = key.split('.', 2)

        if (id != "**" and id != self.last_id) or not self.was_glsl_key_used:
            if self.was_glsl_key_used:
                print(f"{yellow}WARNING: GLSL key: `{self.current_glsl_key}` was already used; Missing define{reset}")
            else:
                entries = self.current_glsl_key.split(',')
                self.compiled_glsl.append("#define " + entries[0].strip() + ' ' + id)
                for entry in entries[1:]:
                    if id == '*':
                        id = "**"
                    self.compiled_glsl.append("#define " + entry.strip() + ' ' + id)
                self.was_glsl_key_used = True

                self.last_id = id

        preprocessed_values = self.pre_process_values(values)

        self.compiled_properties.append(padding + key + '=' + ' '.join(preprocessed_values))

        if id.isdigit():
            self.used_numbers.append(int(id))

        # try:
        if "[" not in line:
            self.potater.append(line.rstrip())
        else:
            parts = line_content.split('=', 1)
            if len(parts) == 2:
                line_content = parts[1].strip()
                result = parts[0] + '='
            else:
                result = ""
            words = line_content.split(' ')
            # new_words = []
            # print(f"found '[' in: {words}")
            for word in words:
                result += ' ' + ' '.join(self.pre_process_values([word]))

            self.potater.append(result)
            #     if '[' in word:
            #         key_properties = word.split(']')
            #         prefix_key = key_properties[0].split('[', 1)
            #         prefix = prefix_key[0]
            #         key = prefix_key[1]
            #         properties = key_properties[1].strip()
            #
            #         if properties[0] != ':':
            #             new_words.append(' '.join(self.pre_process_values([word])))
            #         else:
            #             if key in self.potater_variable_line_splittings:
            #                 # print(f"found '{key}' in 'self.potater_variable_line_splittings': {self.potater_variable_line_splittings[key]}")
            #                 new_key_suffixes = self.potater_variable_line_splittings[key]
            #                 for suffix in new_key_suffixes:
            #                     new_words.append(f"{prefix}[{key}_{suffix}]{properties} \\\n")
            #             else:
            #                 # print(f"'{key}' NOT found in 'self.potater_variable_line_splittings': {self.potater_variable_line_splittings}")
            #                 new_words.append(word)
            #     else:
            #         new_words.append(word)
            #
            # result += ' '.join(new_words).rstrip()
            # if result[-1] == '\\':
            #     result = result[:-2]
            # self.potater.append(result)

        # except Exception as e:
        #     print(f"EXCEPTION: {e}")
        #     self.potater.append(line.rstrip())

    def process_other(self, line: str) -> None:
        line_content = line.strip()
        padding_length = len(line) - len(line_content)
        padding = line[:padding_length - 1]

        preprocessed_values = self.pre_process_values(line_content.split(' '))

        self.compiled_properties.append(padding + ' '.join(preprocessed_values))

        # self.potater.append(line.rstrip())
        line = line.rstrip()
        words = line.split(' ')
        new_words = []
        for word in words:
            new_words.append(' '.join(self.pre_process_values([word])))
        self.potater.append(' '.join(new_words))

    def pre_process_values(self, values: list[str], variable=False, debug=False) -> list[str]:
        processed_values: list[str] = []

        for i, value in enumerate(values):
            if not (value == '\\' and variable and i == len(values) - 1):
                processed_values.extend(flatten(self.pre_process_value(value, variable=variable, debug=debug)))
            else:
                while True:
                    processed_values.append("\\n")
                    next_line_values = self.file.readline().strip().split(' ')
                    break_loop = True
                    for next_line_value in next_line_values:
                        break_loop = True
                        if next_line_value == '\\':
                            break_loop = False
                        else:
                            processed_values.extend(flatten(self.pre_process_value(next_line_value, variable=variable)))
                    if break_loop:
                        break

        # print(f"final {processed_values=}")
        return processed_values

    def pre_process_value(self, value: str, variable=False, debug=False) -> list:
        if '[' in value:
            parts = value.split('[', 1)

            start = parts[0]
            rest = parts[1]

            rest_parts = rest.split(']', 1)

            var_key = rest_parts[0]
            rest = rest_parts[1]

            if not variable:
                self.directly_used_variables.append(var_key)

            variable = self.variables[var_key]

            new_values = []
            for v in variable:
                if v == "\\n" or v == '\n' or v == '\\\n':
                    new_values.append('\\\n')
                elif v == '':
                    print(f"{yellow}WARNING: Empty value{reset}")
                else:
                    new_values.append(self.pre_process_value(start + v + rest))

            return new_values

        else:
            if debug:
                print(f"final {value=}")
            return [value]

    line_processing_function: dict[LineType, Callable[[Self, str], None]] = {
        LineType.COMMENT: process_comment,
        LineType.DEFINE_COMMENT: process_define_comment,
        LineType.IPROPERTY_COMMENT: process_iproperty_comment,
        LineType.GLSL_COMMENT: process_glsl_comment,
        LineType.VARIABLE: process_variable,
        LineType.PROPERTY_DECLARATION: process_property_declaration,
        LineType.OTHER: process_other,
        LineType.EMPTY_LINE: process_empty_line
    }


def compile_properties(args: ArgsNamespace) -> None:
    print(f"{bold}{it}{blue}Preprocessing properties files...{reset}")
    files: list[tuple[tuple[str, str], tuple[str, str, str]]] = []

    if args.block:
        files.append((
            ("block.iProperties.properties", "block.template.properties"),
            ("block.properties", "blocks.glsl", "block.PoTater.properties")
        ))
    if args.item:
        files.append((
            ("item.iProperties.properties", "item.template.properties"),
            ("item.properties", "items.glsl", "item.PoTater.properties")
        ))
    if args.entity:
        files.append((
            ("entity.iProperties.properties", "entity.template.properties"),
            ("entity.properties", "entities.glsl", "entity.PoTater.properties")
        ))

    if not (args.input == "./" or args.input == ""):
        for i, file in enumerate(files):
            new_inputs = []
            for input in file[0]:
                new_inputs.append(f"{args.input}{input}")
            files[i] = (tuple(new_inputs), file[1])

    for file in files:
        print()

        template_file_name = file[0][0]

        # Check if file exists
        if not os.path.exists(template_file_name):
            template_file_name = file[0][1]
            if not os.path.exists(template_file_name):
                print(f"{red}File `{file[0]}` not found!{reset}")
                continue

        print(f"{bold}{blue}Preprocessing: `{template_file_name}`...{reset}")

        preprocessed_properties_text: str
        preprocessed_glsl_text: str

        with open(template_file_name, "r") as f:
            compiler = Preprocessor(f)

            preprocessed_properties_text = compiler.get_compiled_properties()
            preprocessed_glsl_text = compiler.get_compiled_glsl()

            potater_text = compiler.get_potater()

            # print(compiler.variables)

        path: str
        # .properties
        if args.properties:
            if args.properties_output is None:
                path = f"{args.output}{file[1][0]}"
            else:
                path = f"{args.properties_output}{file[1][0]}"

            with open(path, "w") as f:
                f.write(preprocessed_properties_text)
                print(f"{blue}`{file[1][0]}` saved{reset}")

        # .glsl
        if args.glsl:
            if args.glsl_output is None:
                path = f"{args.output}{file[1][1]}"
            else:
                path = f"{args.glsl_output}{file[1][1]}"

            with open(path, "w") as f:
                f.write(preprocessed_glsl_text)
                print(f"{blue}`{file[1][1]}` saved{reset}")

        # .potater
        if args.potater:
            if args.potater_output is None:
                path = f"{args.output}{file[1][2]}"
            else:
                path = f"{args.potater_output}{file[1][2]}"

            with open(path, "w") as f:
                f.write(potater_text)
                print(f"{blue}`{file[1][2]}` saved{reset}")


def flatten(not_flat_list: list) -> list[str]:
    flat: list[str] = []
    almost_flat = almost_flatten(not_flat_list)
    for value in almost_flat:
        flat.append(''.join(value))
    return flat


def almost_flatten(l: list) -> list[list[str]]:
    flat = sum(map(almost_flatten, l), []) if isinstance(l, list) else [l]
    return flat
