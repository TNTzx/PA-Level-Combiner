"""Builds the zip file for release."""


import os
import os.path as osp

import re
import zipfile as zipf


CURRENT_DIR = osp.abspath(osp.dirname(osp.realpath(__file__)))
REPO_DIR = osp.abspath(osp.join(CURRENT_DIR, ".."))
OUTPUT_DIR = osp.abspath(osp.join(CURRENT_DIR, "..", "build"))
if not osp.exists(OUTPUT_DIR):
    os.mkdir(OUTPUT_DIR)


def get_all_file_paths_in_folder(folder_path: str):
    """Gets all the file paths inside a folder."""
    file_paths: list[str] = []
    for new_folder_path, folders_in_folder, files_in_folder in os.walk(folder_path):
        for file_path in files_in_folder:
            file_paths.append(osp.join(new_folder_path, file_path))


    return file_paths

build_version = input("Input level version (no v): ")
OUTPUT_ZIP = osp.join(OUTPUT_DIR, f"PA Level Combiner v{build_version}.zip")



with zipf.ZipFile(OUTPUT_ZIP, "w") as zip_file:
    def write_folder(folder_path: str, zip_folder_path: str = None, path_exclude_regex: str = r"__pycache__", verbose: bool = True):
        """Writes a folder to the zip file."""
        if zip_folder_path is None:
            zip_folder_path = folder_path.split(os.sep)[-1]

        path_exclude_compile = re.compile(path_exclude_regex)

        file_paths = get_all_file_paths_in_folder(folder_path)
        for file_path in file_paths:
            if bool(path_exclude_compile.search(file_path)):
                continue

            file_split_path = file_path.split(os.sep)
            folder_split_path = folder_path.split(os.sep)

            file_split_path = file_split_path[-(len(file_split_path) - len(folder_split_path)):]

            file_split_path.insert(0, zip_folder_path)
            final_zip_folder_path = os.path.join(*file_split_path)

            if verbose:
                print(f"Writing: {file_path}")

            zip_file.write(file_path, final_zip_folder_path)


    def get_relative_dir(folder_name: str):
        """Gets the relative directory path."""
        return osp.join(REPO_DIR, folder_name)


    write_folder(get_relative_dir(".py_embedded"))
    write_folder(get_relative_dir("code"), path_exclude_regex = r"(__pycache__)|(archive)|(testcode.py)")
    write_folder(get_relative_dir("setup"))
    zip_file.write(get_relative_dir("README.md"), "README.md")

input("Finished. Press Enter to Exit.")
