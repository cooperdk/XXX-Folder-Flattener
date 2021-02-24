# XXX Folder Flattener

#### A cross-platform utility to flatten adult video scene directories

#### Will work from an input directory and move all files below the parent subfolders to the parent subfolder, and delete any trash files (configurable in flatten-config.json)


## ARGUMENTS:


-h, --help: Prints this help text

-s, --simulate: Simulates the operation, nothing is deleted or moved. Run this first if unsure of what will happen

-v, --verbose: Verbosity on (lots of text will be printed, pass it to a log by ending the command with " > log.txt"

-f, --force-rmdir: Removes subdirectories below the various main directories, even if not empty (there may be additional residual files besides those in the trash list)

-d (dir), --directory (dir): Pass the working directory to the program with this argument.
  
## EXAMPLE:


`flatten -v -d /folder/xxxclips`

(will simulate traversal of /folder/xxxclips and print verbose output.

Any files within subdirectories of /folder/xxxclips will be moved to that subdirectory.

For example, if you have a folder named /folder/xxxclips/ALSScan and this folder has ten subfolders each with a video file and a .txt and .nfo file, Flatten will remove the .txt and .nfo file and move the video file of each directory to /folder/xxxclips/ALSScan. The subdirectories will be removed if empty (if you had added the -f parameter, it would remove the folder even if there are additional files within them).
For each operation, this command would print the action taken.

The utility prints statistics when done (files moved and files/directories deleted, as well as disk space saved by file deletion).

### Calling from Python application

Send the command line parameters to the utility's main function as a list. Like:

```
import flatten
x = flatten.main(['-v', '-d', '/folder/xxxclips'])
```

Remember, if you're running on Windows, you must pass the escaped path.

