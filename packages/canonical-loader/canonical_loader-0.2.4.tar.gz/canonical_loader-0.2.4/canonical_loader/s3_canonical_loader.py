from .base_canonical_loader import BaseCanonicalLoader
from aws_s3_controller import open_df_in_bucket_by_regex, open_excel_in_bucket_by_regex, scan_files_in_bucket_by_regex

class S3CanonicalLoader(BaseCanonicalLoader):
    """
    S3 implementation of CanonicalLoader.
    Loads files from AWS S3 bucket.
    """
    
    def __init__(self, regex, bucket, bucket_prefix):
        """
        Initialize S3CanonicalLoader.
        
        Args:
            regex (str): Regular expression pattern to match files
            bucket (str): S3 bucket name
            bucket_prefix (str): S3 bucket prefix (folder path)
        """
        self.bucket = bucket
        self.bucket_prefix = bucket_prefix
        super().__init__(regex=regex)
        
        
    def get_families_of_file_name(self):
        """
        Get list of files matching the regex pattern from S3 bucket.
        """
        if self.families is None:
            self.families = scan_files_in_bucket_by_regex(bucket=self.bucket, bucket_prefix=self.bucket_prefix, regex=self.regex, option='name')
        return self.families



    def get_df(self):
        """
        Load dataframe from S3 bucket.
        """
        if self.df is None:
            if self.file_extension == 'csv':
                self.df = open_df_in_bucket_by_regex(bucket=self.bucket, bucket_prefix=self.bucket_prefix, regex=self.file_name)
            elif self.file_extension in ['xls', 'xlsx']:
                self.df = open_excel_in_bucket_by_regex(bucket=self.bucket, bucket_prefix=self.bucket_prefix, regex=self.file_name)
        return self.df



    def get_meta_data(self):
        """
        Get metadata including S3 bucket information.
        """
        meta_data = super().get_meta_data()
        if meta_data is not None:
            meta_data['bucket'] = self.bucket
            meta_data['bucket_prefix'] = self.bucket_prefix
        return meta_data

        



    def save_data_as_df(self, output_folder='dataset-canon', include_index=True, korean_support=True):
        """
        Save processed data as a DataFrame in canonical format.
        For S3 implementation, this still saves to local file system.
        
        Args:
            output_folder (str): Folder to save the output file
            include_index (bool): Whether to include index in the saved file
            korean_support (bool): Whether to enable Korean language support
        """
        return super().save_data_as_df(output_folder, include_index, korean_support)
