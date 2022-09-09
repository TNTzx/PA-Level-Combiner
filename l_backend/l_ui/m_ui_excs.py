"""Contains exceptions."""


from .. import m_base_exc


class UIException(m_base_exc.CombinerException):
    """Base UI exception class."""


class VersionNotSelected(UIException):
    """There are no level folders imported."""
    def __init__(self):
        super().__init__("There's no version selected.")

class NoLevelFolders(UIException):
    """There are no level folders imported."""
    def __init__(self):
        super().__init__("There are no level folders imported.")

class NoOutputPath(UIException):
    """There's no output path'."""
    def __init__(self):
        super().__init__("There's no specified output level folder.")


class GetCombineJobException(UIException):
    """An exception occurred in the combine job exception."""
