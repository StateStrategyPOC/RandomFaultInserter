"""
1. Given a Java project's java src directory and a package in that directory it randomly selects a class in the package
2. Given the class selected in the step before, it selects a line to put the fault into
3. Given the line selected in the step before, it inserts the fault in the form of an action propagation of an error action
4. All the steps before are repeated as many times as desired

Note that this script does refer to either the Client and Server projects in the Github organization this script's project
refers to
"""

import os
import os.path
import random
import sys


class FaultInserter():
    def __init__(self, jave_package_path, fault_shape):
        self.jave_package_path = jave_package_path
        self.fault_shape = fault_shape
        self.selected_class = None
        self.selected_line = None
        self.pick_class()
        self.pick_line()
        self.insert_fault()

    def pick_class(self):
        classes_in_package = [class_path for class_path in os.listdir(self.jave_package_path) if os.path.isfile(object)]
        selected_class = random.randint(0, len(classes_in_package) - 1)
        self.selected_class = classes_in_package[selected_class]

    def pick_line(self):
        lines_count = 0
        with open(self.selected_class) as f:
            for lines_count, l in enumerate(f):
                pass
            lines_count += 1
        self.selected_line = random.randint(0, lines_count)

    def insert_fault(self):
        with open(self.selected_class) as f:
            lines = f.readlines()
        lines_to_write = lines[:self.selected_line] + [self.fault_shape + "\n"] + lines[self.selected_line + 1:]
        with open(self.selected_class, "w") as f:
            f.writelines(lines_to_write)


def main():
    args = sys.argv
    if len(args) != 3:
        print("THIS SCRIPT REQUIRES THE FOLLOWING ARGS: [PATH_TO_PACKAGE_DIR], [FAULT_SHAPE]")
    else:
        if args[1] == "" or args[2] == "":
            print("THIS SCRIPT REQUIRES NON EMPTY ARGS")
            exit(-1)
        if not (os.path.isdir(args[1])):
            print("THIS SCRIPT REQUIRES A VALID PACKAGE DIR PATH")
            exit(-1)
        FaultInserter(args[1], args[2])


if __name__ == '__main__':
    main()
