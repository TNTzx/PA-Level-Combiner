"""Contains a combine job."""


import l_pa_cls_simple


class CombineJob(l_pa_cls_simple.PAObject):
    """Represents a combine job."""
    def __init__(
            self,
            version: type[l_pa_cls_simple.PAVersion] = l_pa_cls_simple.v20_4_4,
            level_folder_paths: list[str] = None,
            base_level_folder_path: str | None = None,
            output_folder_path: str | None = None,
            combine_settings: l_pa_cls_simple.CombineSettings = l_pa_cls_simple.CombineSettings(),
        ):
        if level_folder_paths is None:
            level_folder_paths = []

        self.level_folder_paths = level_folder_paths
        self.base_level_folder_path = base_level_folder_path
        self.output_folder_path = output_folder_path
        self.combine_settings = combine_settings


    def run_job(self):
        """Runs the job."""
        level_folders = [l_pa_cls_simple.LevelFolder.from_folder(path) for path in self.level_folder_paths]
        base_level = l_pa_cls_simple.LevelFolder.from_folder(self.base_level_folder_path) if self.base_level_folder_path is not None else None

        combined = l_pa_cls_simple.LevelFolder.combine_folders(
            level_folders = level_folders,
            primary_level_folder = base_level,
            combine_settings = self.combine_settings
        )

        combined.to_folder(self.output_folder_path)
