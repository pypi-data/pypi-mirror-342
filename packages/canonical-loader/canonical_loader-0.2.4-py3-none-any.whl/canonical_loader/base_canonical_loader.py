from abc import ABC, abstractmethod
from shining_pebbles import get_today
from .general_utils import extract_save_date_in_file_name, extract_date_ref_in_file_name, extract_start_date_in_file_name, extract_end_date_in_file_name, extract_initial_date_in_file_name, extract_final_date_in_file_name
from .general_utils import map_df_to_csv_for_canonicality, map_df_to_data_for_canonicality, map_data_to_df_for_canonicality
from tqdm import tqdm

class BaseCanonicalLoader(ABC):
    def __init__(self, regex, **kwargs):
        """
        Initialize the BaseCanonicalLoader abstract base class.
        
        Args:
            regex (str): Regular expression pattern to match files
            **kwargs: Additional keyword arguments for subclasses
        """
        self.regex = regex
        self.families = None
        self.file_name = None
        self.file_name_prefix = None
        self.date_save = None
        self.date_ref = None
        self.start_date = None
        self.end_date = None
        self.initial_date = None
        self.final_date = None
        self.dates = None
        self.file_extension = None
        self.file_name_format = None
        self.df = None
        self.data = None
        self.meta_data = None
        self.df_reloaded = None
        self._load_pipelines()
        
        
    @abstractmethod
    def get_families_of_file_name(self):
        """Get list of files matching the regex pattern.
        This method should be implemented by subclasses.
        """
        pass

    def get_file_name(self):
        if self.file_name is None:
            self.file_name = self.families[-1]
        return self.file_name

    def get_file_format(self):
        if self.file_name is None:
            self.get_file_name()
        self.file_extension = self.file_name.split('.')[-1]
        
    
    def get_dates(self):
        if self.dates is None:
            if self.file_name is None:
                self.get_file_name()
            self.date_save = extract_save_date_in_file_name(self.file_name)
            if '-at' in self.file_name:
                self.date_ref = extract_date_ref_in_file_name(self.file_name)
                file_name_prefix = self.file_name.split('-at')[0]
            if '-from' in self.file_name:
                self.start_date = extract_start_date_in_file_name(self.file_name)
                self.end_date = extract_end_date_in_file_name(self.file_name)
                file_name_prefix = self.file_name.split('-from')[0]
            if '-between' in self.file_name:
                self.initial_date = extract_initial_date_in_file_name(self.file_name)
                self.final_date = extract_final_date_in_file_name(self.file_name)
                file_name_prefix = self.file_name.split('-between')[0]
            self.dates = {
                'save': self.date_save,
                'ref': self.date_ref,
                'start': self.start_date,
                'end': self.end_date,
                'initial': self.initial_date,
                'final': self.final_date,
            }
            self.file_name_prefix = file_name_prefix.replace('dataset-', '').replace('json-', '')
        return self.dates

    def get_file_name_format(self):
        if self.file_name_format is None:
            if self.file_name is None:
                self.get_file_name()
            if self.dates is None:
                self.get_dates()
            self.file_extension = self.file_name.split('.')[-1]
        mapping_prefix = {
            'csv': 'dataset-',
            'json': 'json-',
        }
        file_name_format = mapping_prefix[self.file_extension] + self.file_name_prefix
        if self.date_ref is not None:
            file_name_format += f'-at{self.date_ref}'
        elif self.start_date is not None:
            file_name_format += f'-from{self.start_date}-to{self.end_date}'
        elif self.initial_date is not None:
            file_name_format += f'-between{self.initial_date}-and{self.final_date}'

        file_name_format += f'-save{get_today().replace("-", "")}.{self.file_extension}'
        self.file_name_format = file_name_format
        return self.file_name_format

    @abstractmethod
    def get_df(self):
        """Load dataframe from file.
        This method should be implemented by subclasses.
        """
        pass

    def get_data(self):
        if self.data is None:
            self.data = map_df_to_data_for_canonicality(self.df)
        return self.data

    def get_meta_data(self):
        """Get metadata about the loaded file.
        This method can be extended by subclasses to add additional metadata.
        """
        if self.meta_data is None:
            self.meta_data = {
                'file_name': self.file_name,
                'file_name_format': self.file_name_format,
                'file_extension': self.file_extension,
                'dates': self.dates,
                'columns': self.df.columns.tolist(),
            }
        return self.meta_data

    def _load_pipelines(self):
        print(f'Loading pipelines with regex {self.regex}')
        pipelines = [
            self.get_families_of_file_name,
            self.get_file_name,
            self.get_file_name_format,
            self.get_df,
            self.get_data,
            self.get_meta_data,
        ]
        for pipeline in tqdm(pipelines):
            print(f'Loading {pipeline.__name__}')
            pipeline()

        return pipelines        

    def reload_df_from_data(self):
        df_reloaded = map_data_to_df_for_canonicality(self.data)
        df_reloaded.index.name = self.df.index.name
        self.df_reloaded = df_reloaded
        return df_reloaded

    def save_data_as_df(self, output_folder='dataset-canon', include_index=True, korean_support=True):
        """
        Save processed data as a DataFrame in canonical format.
        
        Args:
            output_folder (str): Folder to save the output file
            include_index (bool): Whether to include index in the saved file
            korean_support (bool): Whether to enable Korean language support
        """
        if self.df_reloaded is None:
            self.reload_df_from_data()
        map_df_to_csv_for_canonicality(
            self.df_reloaded, 
            file_folder=output_folder, 
            file_name=self.file_name_format, 
            option_including_index=include_index, 
            option_korean=korean_support
        )
        return None
