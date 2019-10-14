# email_extractor
Quick Python 2.7 script for MacOS (including a Mac Automator app) used to extract unique emails from CSV files.

I built this to help our marketing team deal with some CSV files they had received. These CSV files had headers, so I designed the script to handle CSVs with headers. This allows me to also try to grab first and last names from the file. It's certainly possible to modify the script a bit to deal with CSV files without headers.

The Automator app allows you to drag and drop a file or folder onto the app, which MacOS doesn't allow with just a script.

NOTE: This won't work on Windows as is, because the destination directory won't work.
