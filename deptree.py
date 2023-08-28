#!/bin/env python3

import argparse
import subprocess
import os

SUPPORTED_PRINT_FORMATS = ['dot', 'list-newline']

visited_dependencies = []

def get_library_full_path(lib):
    return ''

def parse_ldd_output(output):
    deps = []
    lines = output.split('\n')
    for line in lines:
        components = line.split(' ')

        if len(components) != 4:
            continue

        deps.append(components[2])

    return deps


def get_binary_dependencies(binary):
    proc = subprocess.run(['ldd', binary], capture_output=True)
    
    if proc.returncode != 0:
        print(f'deptree: could not get dependencies for {binary}')
        print(f'{proc.stderr}')
        return []
    
    return parse_ldd_output(proc.stdout.decode('utf-8'))

def print_dependencies_recursivelly(binary, full_path):
    deps = get_binary_dependencies(binary)

    visited_dependencies.append(binary)

    for dependency in deps:
        if full_path == True:
            print(f'"{binary}" -> "{dependency}"')
        else:
            bin_basename = os.path.basename(binary)
            dep_basename = os.path.basename(dependency)
            print(f'"{bin_basename}" -> "{dep_basename}"')

        if dependency in visited_dependencies:
            return
        print_dependencies_recursivelly(dependency, full_path)

def main():
    parser = argparse.ArgumentParser(prog='deptree',
                                     description='Tracks dependencies of elf files',
                                     epilog='https://github.com/IkerGalardi/deptree')
    parser.add_argument('elf')
    parser.add_argument('-f', '--format')
    parser.add_argument('-p', '--print-full-path', action='store_true')

    arguments = parser.parse_args()

    if not (arguments.format in SUPPORTED_PRINT_FORMATS):
        print(f'deptree: format \'{arguments.format}\' is not supported, try {SUPPORTED_PRINT_FORMATS} formats instead')

    if arguments.format == 'dot':
        print_dependencies_recursivelly(arguments.elf, arguments.print_full_path)
    elif arguments.format == 'list-newline':
        print('deptree: not implemented yet')

if __name__ == '__main__':
    main()