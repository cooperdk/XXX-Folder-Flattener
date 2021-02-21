import os, sys, getopt
from pathlib import Path
import json
import shutil

def getConfig() -> dict:
# This function reads the trash file extensions from JSON
    thisdir = os.path.dirname(__file__)
    with open(os.path.abspath(os.path.join(thisdir,'flatten-config.json')), 'r') as config:
        data = config.read()
    
    settings = json.loads(data)    
    configuration = settings
    return configuration

def printDirectoryFiles(directory: str, root: str):
    global removefile, movefile, removepath, pathnotdel, simulate, verbose
    rootdir = root
    extensions = getConfig()
    #print("")
    #print(f"Simulate: {simulate}")
    for filename in os.listdir(directory):  
        full_path=os.path.abspath(os.path.join(directory, filename))
        if not os.path.isdir(full_path):
            #print(f"===> TESTING    : {full_path}")
            for i in extensions['remove-files']:
                if Path(full_path).suffix == "."+i:
                    if not simulate:
                        os.remove(full_path)
                        print(f"--- Removed file:\n{full_path}")
                    else:
                        print(f"--- Would remove file:\n{full_path}")
                    removefile += 1
            for v in extensions['files-to-move']:
                if Path(full_path).suffix == "."+v:
                    if not simulate:
                        shutil.move(full_path, os.path.join(rootdir,os.path.basename(full_path)))
                        print(f">>> Moved file:\n{full_path}\nto {os.path.join(rootdir,os.path.basename(full_path))}")
                    else:
                        print(f">>> Would move file:\n{full_path}\nto {os.path.join(rootdir,os.path.basename(full_path))}")
                    movefile += 1
        else:
            if not os.listdir(full_path):
                if not simulate:
                    os.rmdir(full_path)
                    print(f"--- Removed dir:\n{full_path}")
                else:
                    print(f"--- Would remove dir:\n{full_path}")
                removepath += 1
            else:
                print("Not able to delete dir:\n{full_path}")
                pathnotdel += 1

def checkFolders(directory: str):
# This function checks all root folders within the selected folder.
# These are the folders that video scene files should be moved to.
#
# The root variable makes sure that any video scenes recursively are moved to the main folder 
# (the one directly below the defined starting directory).

    dir_list = next(os.walk(directory))[1]

    #print(dir_list)

    for dir in dir_list:           
        print(f"\nTHIS ROOT IS -> {dir}")
        root = os.path.abspath(os.path.join(directory,dir))
        checkSubFolders(os.path.abspath(os.path.join(directory,dir)), root) 

    #printDirectoryFiles(directory)       


def checkSubFolders(directory: str, root: str):
# This function checks all folders within the calling root folder (recursively)
# To ensure that the files are moved to the first subfolder (read above), the original root is passed on.

    dir_list = next(os.walk(directory))[1]

    #print(dir_list)

    for dir in dir_list:           
        print(f"\nTHIS SUBDIR IS -> {dir}")
        checkSubFolders(directory +"/"+ dir, root) 

    printDirectoryFiles(directory, root)       

def printhelp():
    print ("FLATTEN 0.6")
    print ("===========")
    print ("")
    print ("A utility to flatten adult video scene directories")
    print ("Will work from an input directory and move all files below the parent subfolders")
    print ("to the parent subfolder, and delete any trash files (configurable in flatten-config.json)")
    print ("")
    print ("ARGUMENTS:")
    print ("----------")
    print ("")
    print ("-h, --help:        Prints this help text")
    print ("-s, --simulate:    Simulates the operation, nothing is deleted or moved")
    print ("-v, --verbose:     Verbosity on (lots of text will be printed, pass it to a log by ending")
    print ("                   the command with \" > log.txt\"")
    print ("-d <dir>,")
    print ("--directory <dir>: Pass the working directory to the program with this argument.")
    print ("")
    print ("EXAMPLE:")
    print ("--------")
    print ("")
    print ("flatten -s -v -d /folder/xxxclips")
    print ("(will simulate traversal of /folder/xxxclips and print verbose output.")
    
    
#global removefile, movefile, removepath
removefile = 0
movefile = 0
removepath = 0
pathnotdel = 0
verbose = False
simulate = False
path = ""
argument_list = sys.argv[1:]

short_options = "hd:vs"
long_options = ["help", "directory=", "verbose", "simulate"]

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
        print ("Enabling verbose mode")
        verbose = True
    if current_argument in ("-s", "--simulate"):
        print("Simulating operateion")
        simulate = True
    elif current_argument in ("-h", "--help"):
        printhelp()     
        sys.exit(2)
    elif current_argument in ("-d", "--directory"):
        path = current_value
        print (f"Working from {path}")
    

checkFolders(path)
print("")
if simulate:
    print(f"If you had not simulated this operation, Flatten would have:")
    print(f"- Moved {movefile} video scenes.")
    print(f"- Removed {removefile} trash files and {removepath} subfolders (if possible).")
    #print(f"- Not able to remove {pathnotdel} subfolders.")
else:
    print(f"Flatten is now done flattening {path}.")
    print(f"This was completed:")
    print(f"- Moved {movefile} video scenes.")
    print(f"- Removed {removefile} trash files and {removepath} subfolders.")
    print(f"- Not able to remove {pathnotdel} subfolders.")

#input("Press enter to exit ;")