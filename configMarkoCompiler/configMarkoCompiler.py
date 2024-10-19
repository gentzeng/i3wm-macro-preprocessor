#!/bin/python3

import re
import argparse


def merge_lines(lines):
    merged_lines = []
    current_line = ''

    for line in lines:
        stripped_line = line.rstrip('\n')
        if stripped_line.endswith('\\'):
            current_line += stripped_line[:-1]
        else:
            current_line += stripped_line
            merged_lines.append(current_line)
            current_line = ''

    if current_line:
        merged_lines.append(current_line)

    return merged_lines


def replace_variables(lines):
    variables = {}
    linesSetDollarOn = []
    linesSubstituted = []
    linesSetDollarOff = []

    # change $-sign for set rules
    for line in lines:
        newLine = re.sub('set(\\s*)\\$', 'set\\1--DOLLAR--', line)
        linesSetDollarOn.append(newLine)

    # scan for variable declarations
    for line in linesSetDollarOn:
        match = re.match(r'(?:\s*)set(?:\s*)--DOLLAR--(\w+)(?:\s*)(.+)', line)
        if not match:
            continue
        var_name = match.group(1)
        var_value = match.group(2).strip().replace('${', '').replace('}', '')
        variables[var_name] = var_value

    # replace the variables
    for index, line in enumerate(linesSetDollarOn):
        if '#' not in line:
            newLine = line
            comment = ''
        else:
            lineMatch = re.match(r'(.*?)((?<!\\)#.*)', line)
            newLine = lineMatch.group(1)
            comment = lineMatch.group(2)

        while re.search(r'(?<!\\)\$(?!\()', newLine):
            for var_name, var_value in variables.items():
                if not re.search(r'(?<!\\)\$(?!\()', newLine):
                    break
                rep = re.compile(fr'(?<!\\)\${var_name}\b')
                newLine = re.sub(rep, var_value, newLine)
        linesSubstituted.append(f'{newLine}{comment}')

    # unchange $-sign for set rules
    for line in linesSubstituted:
        newLine = re.sub('set(\\s*)--DOLLAR--', 'set\\1$', line)
        linesSetDollarOff.append(newLine)

    return linesSetDollarOff


def resolve_makros(lines):
    """
    Makro definitions need to have at least one
    space character after the #define tag. The rest of the line serves
    as the definition.
    """
    makros = {}
    linesSubstituted = []

    #scan for makro definitions
    for line in lines:
        match = re.match(r'(?:\s*)#define (\w+)(?:\s+?)(.+)', line)
        if not match:
            continue
        makro_name = match.group(1)
        makro_value = match.group(2).rstrip()
        makros[makro_name] = makro_value

    #delete all lines with #define
    pattern = re.compile("#define")

    filtered_lines = [line for line in lines if not pattern.search(line)]

    for line in filtered_lines:
        for makro_name, makro_value in makros.items():
            line = line.replace(f'{makro_name}', makro_value )
        linesSubstituted.append(line)

    return linesSubstituted


def main():
    parser = argparse.ArgumentParser(
        description='Replace variables in i3 config.'
    )
    parser.add_argument(
        'config_path',
        metavar='CONFIG_PATH',
        type=str,
        help='Path to the i3 config file'
    )
    args = parser.parse_args()

    with open(args.config_path, 'r') as f:
        lines = f.readlines()

    lines = merge_lines(lines)
    lines = resolve_makros(lines)
    lines = replace_variables(lines)

    with open(args.config_path, 'w') as f:
        f.writelines(line + '\n' for line in lines)


if __name__ == '__main__':
    main()
