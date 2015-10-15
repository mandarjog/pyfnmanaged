#!/usr/bin/env python

"""
example of how behaviour can be changed
at runtime.
"""

import fnmanaged


@fnmanaged.managed
def grepfile(filename, needle):
    matches = 0
    for idx, line in enumerate(open(filename, "rt")):
        if needle in line:
            print "{}:{}".format(filename, idx), line.strip()
            matches += 1
    return matches


def main(args):
    if len(args) < 2:
        print "./pygrep.py string_to_find  file1 file2 ..."
        print "FN_MANAGED=async ./pygrep.py string_to_find  file1 file2 ..."
        return -1

    needle = args[0]
    filenames = args[1:]
    matches = [grepfile(filename, needle) for filename in filenames]

    total = sum(matches)
    print 25 * "*"
    print "Total files:", len(filenames)
    print "Total matches:", total
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main(sys.argv[1:]))
