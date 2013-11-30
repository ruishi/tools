################################################################################
#author: RD Galang
#desc: batch renames files by removing a certain type of character specified by
#      the user
#TODO: -change directory to an optional argument, indicating that the working
#       directory is to be used
################################################################################

import os, sys
import argparse
import glob

def rename(directory, criteria, filetype = None):
    """Renames all the files in a given directory based on user criteria.

    Keyword arguments:
    directory - the path to the directory in which the files should be renamed
    criteria - the criteria for the renaming. currently removes everything but
               the criteria. ex: if criteria is 'alpha' all non-alpha 
               characters are removed.
    filetype - optional parameter that allows the user to specify a target
               filetype. ex: a user can choose to rename only .mp3 files in the
               directory.

    Returns: None"""

    if directory[-1] != os.sep:
        directory += os.sep

    if filetype:
        files = [x for x in glob.glob(directory + '*' + filetype)]
    else:
        files = [x for x in glob.glob(directory + '*') if os.path.isfile(x)]

    for f in files:
        filename = os.path.split(f)[1]
        name, filetype = os.path.splitext(filename)
        if criteria == 'alphanum':
            newname = ''.join([x for x in name if x.isalnum()])
            if len(newname) == 0:
                print("Renaming " + filename + " results in invalid filename."
                      + " Skipping rename.")
                newname = name
        elif criteria == 'alpha':
            newname = ''.join([x for x in name if x.isalpha()])
            if len(newname) == 0:
                print("Renaming " + filename + " results in invalid filename."
                      + " Skipping rename.")
                newname = name
        elif criteria == 'num':
            newname = ''.join([x for x in name if x.isdigit()])
            if len(newname) == 0:
                print("Renaming " + filename + " results in invalid filename."
                      + " Skipping rename.")
                newname = name
        newfile = os.path.join(directory, newname + filetype)
        os.rename(f, newfile)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Process filename options")
    parser.add_argument('input', help="path to desired directory")
    parser.add_argument('-t', '--type', help="specify file type to target")
    parser.add_argument('criteria', help="specify removal criteria")
    args = parser.parse_args()

    if args.type:
        rename(args.input, args.criteria, args.type)
    else:
        rename(args.input, args.criteria)
