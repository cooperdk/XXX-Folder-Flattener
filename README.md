# XXX Folder Flattener

#### A cross-platform utility to flatten adult video scene directories

#### Will work from an input directory and move all files below the parent subfolders to the parent subfolder, and delete any trash files (configurable in flatten-config.json)


## ARGUMENTS:


-h, --help: Prints this help text

-s, --simulate: Simulates the operation, nothing is deleted or moved

-v, --verbose: Verbosity on (lots of text will be printed, pass it to a log by ending the command with " > log.txt"

-f, --force-rmdir: Removes subdirectories below the various main directories, even if not empty (there may be additional residual files besides those in the trash list)

-d (dir), --directory (dir): Pass the working directory to the program with this argument.
  
## EXAMPLE:


`flatten -s -v -d /folder/xxxclips`

(will simulate traversal of /folder/xxxclips and print verbose output.


Some functionality not yet done, verbosity will print out a huge load of text.

The utility prints statistics when done.

### Calling from Python application

Send the command line parameters to the utility's main function as a list. Like:

```
import flatten
x = flatten.main(['-s', '-v', '-d', '/folder/xxxclips'])
```

Remember, if you're running on Windows, you must send the directory escaped (with double-backslashes).

