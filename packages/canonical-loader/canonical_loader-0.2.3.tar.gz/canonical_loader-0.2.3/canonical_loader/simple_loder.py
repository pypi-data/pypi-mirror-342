from shining_pebbles import scan_files_including_regex, load_csv_in_file_folder_by_regex, load_xlsx_in_file_folder_by_regex, load_xls_in_file_folder_by_regex
from canonical_loader.canonic_convert_utils import map_df_to_data_for_canonicality
from string_date_controller import map_date_nondashed_to_dashed

class SimpleLoader:
    def __init__(self, regex, file_folder):
        self.regex = regex
        self.file_folder = file_folder
        self.families = None
        self.file_name = None
        self.file_extension = None
        self.df = None
        self.data = None
        self.date_ref = None
        self.meta_data = None
        self._load_pipelines()

    def get_families_of_file_name(self):
        if self.families is None:
            self.families = scan_files_including_regex(file_folder=self.file_folder, regex=self.regex)
        return self.families

    def get_file_name(self):
        if self.file_name is None:
            self.file_name = self.families[-1]
            self.file_extension = self.file_name.split('.')[-1]
        return self.file_name

    def get_df(self):
        if self.df is None and self.file_name is not None:
            self.get_file_name()
            if self.file_extension == 'csv':
                self.df = load_csv_in_file_folder_by_regex(file_folder=self.file_folder, regex=self.file_name)
            elif self.file_extension == 'xlsx':
                self.df = load_xlsx_in_file_folder_by_regex(file_folder=self.file_folder, regex=self.file_name)
            elif self.file_extension == 'xls':
                self.df = load_xls_in_file_folder_by_regex(file_folder=self.file_folder, regex=self.file_name)
        return self.df

    def get_data(self):
        if self.data is None:
            self.get_df()
            self.data = map_df_to_data_for_canonicality(self.df)
        return self.data
        
    def _load_pipelines(self):
        pipelines = [
            self.get_families_of_file_name,
            self.get_file_name,
            self.get_df,
            self.get_data,
        ]
        for pipeline in pipelines:
            pipeline()
        return pipelines

