"""Contains checks."""


import l_pa_cls_simple

from .. import m_ui_excs


def to_lfolder_import_exc(import_exc: l_pa_cls_simple.ImportException | m_ui_excs.UIException):
    """Raises a `GetCombineJobException` based on the import exception."""
    if isinstance(import_exc, l_pa_cls_simple.FolderNotFound):
        lf_import_exc = m_ui_excs.LevelFolderImportException(
            f"The folder \"{import_exc.not_found_folder}\" can't be found!"
        )
    elif isinstance(import_exc, l_pa_cls_simple.LevelFileNotFound):
        lf_import_exc = m_ui_excs.LevelFolderImportException(
            f"The level folder \"{import_exc.level_folder_path}\" doesn't have the {import_exc.missing_file} file!"
        )
    elif isinstance(import_exc, l_pa_cls_simple.IncompatibleVersionImport):
        lf_import_exc = m_ui_excs.LevelFolderImportException(
            (
                f"The level folder \"{import_exc.level_folder_path}\" with version {import_exc.importing_version_num} "
                f"is not compatible with the currently selected version ({import_exc.current_version_num})."
            )
        )
    else:
        raise ValueError("Import exception not supported.")


    return lf_import_exc


def check_level_folder(version: l_pa_cls_simple.PAVersion, folder_path: str):
    """Checks the level folder. Raises a `LevelFolderImportException` if an error occurs, otherwise returns `True`."""
    try:
        version.import_level_folder(folder_path)
    except l_pa_cls_simple.ImportException as exc:
        raise to_lfolder_import_exc(exc) from exc

    return True
