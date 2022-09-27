# PA Level Combiner

A program that combines two levels of the same song into one.
Used to make collaborations easier by allowing collab members to work on their parts individually instead of passing files around.

## False positive detection! >:(
Some antiviruses might detect the .exe as malicious, but I can guarantee you 100% undeniably and certainly that releases will never ever contain viruses!
The packager, PyInstaller, used to convert my scripts into a `.exe` seems to have this problem. I tried switching to others but to no avail, some even raising the number of false positives.
If you still are really *really* unsure, the code base includes the `build.bat` (which is the program used to execute PyInstaller) and the `.spec` file (used to freeze the program to a `.exe` with specific configurations). Go build it yourself if you're really *really* ***really*** unsure.

## How it's used:
![how it's used](https://i.imgur.com/KNIO3u8.png)
Sometimes, parts of a level are split in different levels. This program combines those levels to get a level with all the parts in it.


## Instructions:
(explained in the `Instructions` button in the program. too lazy to write it all down here, will add in another update)
