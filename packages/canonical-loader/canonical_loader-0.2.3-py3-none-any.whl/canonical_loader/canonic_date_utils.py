
def extract_save_date_in_file_name(file_name):
    return file_name.split('-save')[-1].split('.')[0]

def extract_date_ref_in_file_name(file_name):
    return file_name.split('-at')[-1].split('-')[0]

def extract_start_date_in_file_name(file_name):
    return file_name.split('-from')[-1].split('-')[0]

def extract_end_date_in_file_name(file_name):
    return file_name.split('-to')[-1].split('-')[0]
    
def extract_initial_date_in_file_name(file_name):
    return file_name.split('-between')[-1].split('-')[0]

def extract_final_date_in_file_name(file_name):
    return file_name.split('-and')[-1].split('-')[0]

    