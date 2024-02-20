# DEPRECATED
This repository is deprecated. The new and more improved version is here: https://github.com/PA-Level-Combiner/PA-Level-Combiner-v3

# PA Level Combiner

A program that combines two levels of the same song into one.
Used to make collaborations easier by allowing collab members to work on their parts individually instead of passing files around.

## How to install
1. Download the .zip, then right click and extract the .zip to a folder.
2. Go inside the folder, then open the `setup` folder, then double click on the `setup.bat` file.
3. On the following window, save the shortcut to your favorite folder.
4. Press enter to close the setup.
5. Go to the shortcut, double click, and have fun collaborating!

## How it's used:
![how it's used](https://i.imgur.com/KNIO3u8.png)
Sometimes, parts of a level are split in different levels. This program combines those levels to get a level with all the parts in it.


## Instructions:
(explained in the `Instructions` button in the program. too lazy to write it all down here, will add in another update)



## Setting Up Dev Environment

Make sure you have Python 3.10.1 installed.

### .py_embedded
1. Create a new folder called .py_embedded
2. Download a Python embeddable package from here: https://python.org/downloads/release/python-3101 (Scroll down and select **Windows embeddable package (64-bit)**)
3. Extract all contents to `.py_embedded`

### Setting up Tkinter
4. Open the normal python distribution from `%appdata%\..\Local\Programs\Python\Python310` (we will refer to this path as `normalpython`)
5. Copy the following files and folders and paste them to the `.py_embedded/` folder:
    - `normalpython/tcl`
    - `normalpython/Lib/tkinter`
    - `normalpython/DLLs/`
        - `_tkinter.pyd`
        - `tcl86t.dll`
        - `tk86t.dll`

### Setting up pip
6. Go to `.py_embedded/python310._pth` and delete everything, paste the following:
```
python310.zip
.
../code
# Uncomment to run site.main() automatically
import site
```
7. Install `get_pip.py` from here: https://bootstrap.pypa.io/get-pip.py, save to `.py_embedded`
8. Open command prompt (admin) and `cd` to `.py_embedded`, run `python.exe get-pip.py`
9. Run `".py_embedded/python.exe" -m pip install -r requirements.txt`

### Creating a venv
10. Create a venv using `"%appdata%\..\Local\Programs\Python\Python310\python.exe" -m venv .venv`


## Developing

### Updating dependencies from venv to embeddable
1. Open command prompt, `cd` to the project's folder
2. Run `".venv/Scripts/python" -m pip freeze > requirements.txt`
3. Run `".py_embedded/python.exe" -m pip install -r requirements.txt`

### Building zip
1. Open command prompt, `cd` to the project's folder
2. Run `".venv/Scripts/python" "make_zip/build.py"`
3. A .zip will appear in `build/`.
