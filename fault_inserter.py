#!/usr/bin/env python
"""
1. Given a Java project's java src directory and a package in that directory it randomly selects a class in the package
2. Given the class selected in the step before, it selects a line to put the fault into
3. Given the line selected in the step before, it inserts the fault in the form of an action propagation of an error action
4. All the steps before are repeated as many times as desired

Note that:
1. This script does refer to either the Client and Server projects in the Github organization this script's project
belongs to.
2. This script does not consider java methods without the qualifiers 'public','protected','private'

"""

import os
import random
import sys
import re


class FaultInserter():
    def __init__(self, jave_package_path, fault_shape, iterations, forced_class):
        self.iterations = int(iterations)
        self.method_regex = \
            re.compile('\s*(public |private |protected )(static )?(final )?(synchronized )?(\w* )'
                       '?\w+\(.*\)( throws \w+ )?\s*{\n')
        self.jave_package_path = jave_package_path
        self.forced_class = forced_class
        self.fault_shape = fault_shape
        self.selected_class = None
        self.indexed_methods = []
        for i in range(0,self.iterations):
            self.pick_class()
            self.index_methods()
            self.insert_fault()

    def index_methods(self):
        methods_dicts = []
        starts = None
        par_count = 0
        with open(self.selected_class) as f:
            for index, line in enumerate(f):
                if re.match(self.method_regex, line):
                    starts = index
                    par_count += 1
                elif " class " in line:
                    pass
                else:
                    if '{' in line:
                        par_count += 1
                    if '}' in line:
                        par_count -= 1
                        if par_count == 0 and starts is not None:
                            methods_dicts.append(starts)
                            starts = None
        self.indexed_methods = methods_dicts

    def pick_class(self):
        if self.forced_class is not None:
            self.selected_class = self.forced_class
        else:
            classes_in_package = [class_path for class_path in os.listdir(self.jave_package_path)
                                  if os.path.isfile(self.jave_package_path + "/" + class_path)]
            selected_class = random.randint(0, len(classes_in_package) - 1)
            self.selected_class = self.jave_package_path + "/" + classes_in_package[selected_class]

    def insert_fault(self):
        selected_method = self.indexed_methods[random.randint(0, len(self.indexed_methods) - 1)]
        with open(self.selected_class) as f:
            lines = f.readlines()
        lines_to_write = lines[:selected_method + 1] + [self.fault_shape + "\n"] + lines[selected_method + 1:]
        with open(self.selected_class, "w") as f:
            f.writelines(lines_to_write)
        print(self.selected_class)
        print(selected_method)

def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def main():
    args = sys.argv
    argc = len(args)
    if argc != 4 and argc != 5:
        print("THIS SCRIPT REQUIRES THE FOLLOWING ARGS: [PATH_TO_PACKAGE_DIR] [FAULT_SHAPE] [ITERATIONS] [SPECIFIC_CLASS]?")
    else:
        if args[1] == "" or args[2] == "":
            print("THIS SCRIPT REQUIRES NON EMPTY ARGS")
            exit(-1)
        if not (os.path.isdir(args[1])):
            print("THIS SCRIPT REQUIRES A VALID PACKAGE DIR PATH")
            exit(-1)
        if is_number(args[3]) is False:
            print("THIS SCRIPT REQUIRES A VALID INTEGER NUMBER OF ITERATIONS")
            exit(-1)
        if argc == 5:
            FaultInserter(args[1], args[2], args[3], args[4])
        else:
            FaultInserter(args[1], args[2], args[3],None)


if __name__ == '__main__':
    main()
