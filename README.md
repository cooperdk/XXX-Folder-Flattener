# XXX Folder Flattener

#### A command-line utility to flatten adult video scene directories. Companion tool for [YAPO](https://github.com/cooperdk/YAPO-e-plus) and other porn organizers

#### Will work from an input directory and move all files below the parent subfolders to the parent subfolder, and delete any trash files (configurable in flatten-config.json)

[Get a compiled version of the utility here](https://github.com/cooperdk/XXX-Folder-Flattener/releases)

The app will take a directory and flatten all subdirectories. Also, files of configurable types will be removed in the process, as well as the directories the scenes were originally placed in, if they are empty.

You will have to move files/directories with scenes from your various websites/networks to their individual main directories, the utility will then flatten the directory structure within those directories.

Example:


```
1000 Facials
  -1000 Facials - Ella Knox Blowbang
    -1000Facials - Ella Knox - Ella Knox Blowbang.mp4
    -1000Facials - Ella Knox - Ella Knox Blowbang.txt
    -1000Facials - Ella Knox - Ella Knox Blowbang.nfo
  -1000Facials.18.03.12.Alex.More
    -1000Facials.18.03.12.Alex.More.XXX.SD.MP4.mp4
  -1000Facials.20.11.09.Natasha.Starr
    -1kf.20.11.09.natasha.starr.poor.baby.mp4
ALS Scan
  -ALSSxan.20.09.01.Gina.Gerson.and.Tina.Hot
    -ALSScan.20.09.01.Gina.Gerson.and.Tina.Hot.Spotter.BTS.mp4
    -ALSScan.20.09.01.Gina.Gerson.and.Tina.Hot.Spotter.BTS.nfo
BANG
  -I.Dont.Wanna.Be.Fingered.Gimme.Your.Fist
    -I.Dont.Wanna.Be.Fingered.Gimme.Your.Fist.mp4
```

Will become:

```
1000 Facials
  -1000Facials - Ella Knox - Ella Knox Blowbang.mp4
  -1000Facials.18.03.12.Alex.More.XXX.SD.MP4.mp4
  -1kf.20.11.09.natasha.starr.poor.baby.mp4
ALS Scan
  -ALSScan.20.09.01.Gina.Gerson.and.Tina.Hot.Spotter.BTS.mp4
BANG
  -I.Dont.Wanna.Be.Fingered.Gimme.Your.Fist.mp4
```

This will make it easier to keep an overview of your content, and for organizer software to manage your video clips.


## ARGUMENTS:


-h, --help: Prints this help text

-s, --simulate: Simulates the operation, nothing is deleted or moved

-v, --verbose: Verbosity on (lots of text will be printed, pass it to a log by ending the command with " > log.txt"

-d (dir), --directory (dir): Pass the working directory to the program with this argument.
  
## EXAMPLE:


flatten -s -v -d /folder/xxxclips

(will simulate traversal of /folder/xxxclips and print verbose output.


Some functionality not yet done, the program always runs in verbose mode currently, and verbosity will print out a lot of text.

The utility prints statistics about what it did when it is finished.
