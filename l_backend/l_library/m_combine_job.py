"""Contains a combine job."""


import l_pa_cls_simple


class CombineJob(l_pa_cls_simple.PAObject):
    """Represents a combine job."""
    def __init__(
            self,
            version: type[l_pa_cls_simple.PAVersion] | None = None,
            level_folders: list[l_pa_cls_simple.LevelFolder] = None,
            base_level_folder: l_pa_cls_simple.LevelFolder | None = None,
            output_folder_path: str | None = None,
            combine_settings: l_pa_cls_simple.CombineSettings = l_pa_cls_simple.CombineSettings(),
        ):
        if level_folders is None:
            level_folders = []

        self.version = version
        self.level_folders = level_folders
        self.base_level_folder = base_level_folder
        self.output_folder_path = output_folder_path
        self.combine_settings = combine_settings


    def run_job(self):
        """Runs the job."""
        combined = l_pa_cls_simple.LevelFolder.combine_folders(
            level_folders = self.level_folders,
            primary_level_folder = self.base_level_folder,
            combine_settings = self.combine_settings
        )

        self.version.export_level_folder(combined, self.output_folder_path)
