#!/usr/bin/python3
# pylint: disable=C0301
"""
flatten.py
https://github.com/cooperdk/XXX-Folder-Flattener
"""
import os
import sys
import getopt
from pathlib import Path
import json
import shutil

def getconfig () -> dict:
    """
    This function reads the trash file and allowed video file extensions from a JSON file
    :return:
    """
    thisdir = os.path.dirname(__file__)
    with open(os.path.abspath(os.path.join(thisdir, 'flatten-config.json')), 'r') as config:
        data = config.read()
    return json.loads(data)


def printdirfiles (directory: str, root: str):
    """
    This function works with the individual files and directories and decides, based on settings,
    what is going to happen to them

    :param directory:
    :param root:
    :return:
    """
    global removefile, movefile, removepath, pathnotdel, simulate, verbose, forcermdir,\
           rmsize, mvsize, corrsize
    rootdir = root
    worksize = 0
    extensions = getconfig()

    for filename in os.listdir(directory):
        sys.stdout.flush()
        full_path = os.path.abspath(os.path.join(directory, filename))
        if not os.path.isdir(full_path):
            for i in extensions['remove-files']:
                if Path(full_path).suffix == "." + i:
                    worksize = os.path.getsize(full_path)
                    if not simulate:
                        try:
                            print(f"--- Removing file:\n    {full_path}") if verbose else print("-",end="")
                            os.remove(full_path)
                        except IOError as exc:
                            print(f"!!! Error: {exc}")
                            pass
                    else:
                        print(f"--- Would remove file:\n    {full_path}") if verbose else print("-",end="")
                    rmsize += worksize
                    removefile += 1
            for v in extensions['files-to-move']:
                if Path(full_path).suffix == "." + v and (os.path.abspath(directory) != os.path.abspath(rootdir)):
                    worksize = os.path.getsize(full_path)
                    if not simulate:
                        try:
                            print(
                                f">>> Moving file:\n    {full_path}\n    to "
                                f"{os.path.join(rootdir, os.path.basename(full_path))}") \
                            if verbose else print("+",end="")
                            shutil.move(full_path, os.path.join(rootdir, os.path.basename(full_path)))
                        except OSError as exc:
                            print(f"!!! Error: {exc}")
                            pass
                    else:
                        print(
                            f">>> Would move file:\n    {full_path}\n    to "
                            f"{os.path.join(rootdir, os.path.basename(full_path))}") \
                            if verbose else print("+", end="")
                    mvsize += worksize
                    movefile += 1
                elif Path(full_path).suffix == "." + v and (os.path.abspath(directory) == os.path.abspath(rootdir)):
                    print(f"~~~ Not moving {full_path}\n    "
                          f"(already placed correctly)") if verbose else print("*",end="")
                    corrsize += worksize
        else:
            if not simulate:
                try:
                    print(f"--- Removing dir:\n    {full_path} "
                          f"(force: {forcermdir})") if verbose else print("#",end="")
                    if forcermdir:
                        shutil.rmtree(full_path)
                    else:
                        os.rmdir(full_path)
                    removepath += 1
                except (IOError, OSError) as exc:
                    print(f"!!! Error: {exc}")
                    pathnotdel += 1
                    pass
            else:
                print(f"--- Would remove dir:\n    {full_path} "
                      f"(force: {forcermdir})") if verbose else print("#",end="")
                removepath += 1


def checkFolders (directory: str):
    """
    This function checks all root folders within the selected folder.
    These are the folders that video scene files should be moved to.
    The root variable makes sure that any video scenes recursively are moved to the main folder
    (the one directly below the defined starting directory).

    :param directory:
    :return:
    """

    global verbose
    dir_list = next(os.walk(directory))[1]

    for dir in dir_list:
        print(f"\n\n*** Now in a new parent directory -> {dir}")
        root = os.path.abspath(os.path.join(directory, dir))
        checkSubFolders(os.path.abspath(os.path.join(directory, dir)), root)

        # printdirfiles(directory)


def checkSubFolders (directory: str, root: str):
    """
    This function checks all folders within the calling root folder (recursively)
    To ensure that the files are moved to the first subfolder (read above), the original root is passed on.

    :param directory:
    :param root:
    :return:
    """
    global verbose
    dir_list = next(os.walk(directory))[1]

    for dir in dir_list:
        if verbose: print(f"\n\n*** Now in subdirectory -> {dir}")
        checkSubFolders(directory + "/" + dir, root)

    printdirfiles(directory, root)


def printhelp ():
    # Prints a help text

    print("FLATTEN v0.7.5")
    print("==============")
    print("")
    print("A utility to flatten adult video scene directories")
    print("Will work from an input directory and move all files below the parent subfolders")
    print("to the parent subfolder, and delete any trash files (configurable in flatten-config.json)")
    print("")
    print("ARGUMENTS:")
    print("----------")
    print("")
    print("-h, --help:        Prints this help text")
    print("-l, --legend:      Displays a description of the symbols used to descript operations (non-verbose) ")
    print("-s, --simulate:    Simulates the operation, nothing is deleted or moved")
    print("-v, --verbose:     Verbosity on (lots of text will be printed, pass it to a log by ending")
    print("                   the command with \" > log.txt\"")
    print("-f, --force-rmdir: Removes subdirectories below the various main directories, even if not empty")
    print("                   (there may be additional residual files besides those in the trash list)")
    print("-d <dir>,")
    print("--directory <dir>: Pass the working directory to the program with this argument. No trailing slash!")
    print("")
    print("EXAMPLE:")
    print("--------")
    print("")
    print("flatten -s -v -d /folder/xxxclips")
    print("(will simulate traversal of /folder/xxxclips and print verbose output.")

def get_human_readable_size(num):
    rounded_val = round(0)
    exp_str = [ (0, 'B'), (10, 'KB'),(20, 'MB'),(30, 'GB'),(40, 'TB'), (50, 'PB'),]
    i = 0
    while i+1 < len(exp_str) and num >= (2 ** exp_str[i+1][0]):
        i += 1
        rounded_val = round(float(num) / 2 ** exp_str[i][0], 2)
    return f'{int(rounded_val)} {exp_str[i][1]}'


def main(args: list):
    # This is the main program

    global removefile, movefile, removepath, pathnotdel, simulate, verbose, forcermdir, rmsize, mvsize, corrsize
    removefile = 0
    movefile = 0
    removepath = 0
    pathnotdel = 0
    rmsize = 0
    mvsize = 0
    corrsize = 0
    verbose = False
    simulate = False
    forcermdir = False
    path = ""
    argument_list = args

    short_options = "hld:fvs"
    long_options = ["help", "legend", "directory=", "force-rmdir", "verbose", "simulate"]

    try:
        arguments, values = getopt.getopt(argument_list, short_options, long_options)
    except getopt.error:
        # Output error, and return with an error code
        print("ERROR: Wrong arguments.\nUse -h or --help for help.")
        sys.exit(2)

    if not arguments:
        printhelp()
        sys.exit(2)

    for current_argument, current_value in arguments:
        if current_argument in ("-v", "--verbose"):
            print("Enabling verbose mode")
            verbose = True
        if current_argument in ("-l", "--legend"):
            print("\nOperations legend\n=================\n\n+: Moved file\n-: Deleted trash file\n"
                  "*: Not moved file (placed correctly)\n#: Removed directory\n")
            forcermdir = True
            sys.exit(0)
        if current_argument in ("-s", "--simulate"):
            print("Simulating operation")
            simulate = True
        if current_argument in ("-f", "--force-rmdir"):
            print("Forcing removal of subdirectories")
            forcermdir = True
        elif current_argument in ("-h", "--help"):
            printhelp()
            sys.exit(0)
        elif current_argument in ("-d", "--directory"):
            try:
                path = os.path.abspath(current_value)
            except IOError as exc:
                print(exc)
            print(f"Working from {path}")

    print(os.path.abspath(path))
    checkFolders(path)
    print("")
    if simulate:
        print(f"\nIf you had not simulated this operation, Flatten would have:\n")
        print(f"Moved {movefile} video scenes.")
        print(f"Removed {removefile} trash files and {removepath} subfolders (if possible).\n")
        #print(f"- Not able to remove {pathnotdel} subfolders.")
        print(f"Size of files that would be moved: {get_human_readable_size(mvsize)}")
        print(f"Size of files that would be removed: {get_human_readable_size(rmsize)}")
    else:
        print(f"\nFlatten is now done flattening {path}.")
        print(f"This was completed:\n")
        print(f"Moved {movefile} video scenes.")
        print(f"Removed {removefile} trash files and {removepath} subfolders.")
        print(f"Not able to remove {pathnotdel} subfolders.\n")
        print(f"Size of files that were moved: {get_human_readable_size(mvsize)}")
        print(f"Size of files that were removed: {get_human_readable_size(rmsize)}")
    print(f"Size of files that were already placed at the right location: {get_human_readable_size(corrsize)}")
# rmsize, mvsize, corrsize
if __name__ == "__main__":
    main(sys.argv[1:])
