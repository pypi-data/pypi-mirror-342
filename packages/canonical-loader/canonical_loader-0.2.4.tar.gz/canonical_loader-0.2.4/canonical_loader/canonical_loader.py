from .base_canonical_loader import BaseCanonicalLoader
from shining_pebbles import scan_files_including_regex, load_csv_in_file_folder_by_regex, load_xlsx_in_file_folder_by_regex, load_xls_in_file_folder_by_regex

class CanonicalLoader(BaseCanonicalLoader):
    """
    Local file system implementation of CanonicalLoader.
    Loads files from local file system.
    """
    
    def __init__(self, regex, file_folder):
        """
        Initialize CanonicalLoader.
        
        Args:
            regex (str): Regular expression pattern to match files
            file_folder (str): Local folder path to search for files
        """
        self.file_folder = file_folder
        super().__init__(regex=regex)
    
    def get_families_of_file_name(self):
        """
        Get list of files matching the regex pattern from local file system.
        """
        if self.families is None:
            self.families = scan_files_including_regex(file_folder=self.file_folder, regex=self.regex)
        return self.families
    
    def get_df(self):
        """
        Load dataframe from local file.
        """
        if self.df is None:
            if self.file_extension == 'csv':
                self.df = load_csv_in_file_folder_by_regex(file_folder=self.file_folder, regex=self.file_name)
            elif self.file_extension == 'xlsx':
                self.df = load_xlsx_in_file_folder_by_regex(file_folder=self.file_folder, regex=self.file_name)
            elif self.file_extension == 'xls':
                self.df = load_xls_in_file_folder_by_regex(file_folder=self.file_folder, regex=self.file_name)
        return self.df
    
    def get_meta_data(self):
        """
        Get metadata including local file path information.
        """
        meta_data = super().get_meta_data()
        if meta_data is not None:
            meta_data['file_folder'] = self.file_folder
        return meta_data
