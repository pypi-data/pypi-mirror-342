import requests
import json
import pandas as pd
import os
import logging
from tqdm import tqdm
from multiprocessing import Pool, cpu_count

class DataFetcher:
    BASE_URL = "https://ilthermo.boulder.nist.gov/ILT2"
    
    def __init__(self):
        self.session = requests.Session()
    
    def get_property_data(self, compound_name="", compound_number=2, property_id="JkYu"):
        """Fetch property data from ILThermo database"""
        url = f"{self.BASE_URL}/ilsearch?cmp={compound_name}&ncmp={compound_number}&prp={property_id}"
        response = self.session.get(url)
        return response.json() if response.status_code == 200 else None

    def get_compound_data(self, compound_ids, compounds_csv_path):
        """Get SMILES strings for compound IDs"""
        try:
            df_smiles = pd.read_csv(compounds_csv_path)
            smiles_list = []
            for compound_id in compound_ids:
                smile = df_smiles.loc[df_smiles['id'] == compound_id, 'smiles']
                smiles_list.append(smile.values[0] if not smile.empty else None)
            return smiles_list
        except Exception as e:
            logging.error(f"Error getting SMILES data: {e}")
            return []

class DataProcessor:
    def __init__(self):
        self.data = None
        self.column_mappings = {
            'ref': 'reference',
            'prp': 'property',
            'cmp1': 'compound id 1',
            'cmp2': 'compound id 2',
            'cmp3': 'compound id 3',
            'nm1': 'compound name 1',
            'nm2': 'compound name 2',
            'nm3': 'compound name 3'
        }
    
    def load_json(self, json_data):
        """Load and process JSON data"""
        self.data = pd.json_normalize(json_data)
        return self

    def to_csv(self, output_path):
        """Save processed data to CSV"""
        if self.data is not None:
            self.data.to_csv(output_path, index=False)

    def update_metadata(self, output_csv_path, density_data_csv_path):
        """Update density CSV with metadata"""
        try:
            output_df = pd.read_csv(output_csv_path)
            density_df = pd.read_csv(density_data_csv_path)
            
            output_dict = output_df.set_index('setid').to_dict('index')
            
            for index, row in density_df.iterrows():
                set_id = row['setid']
                if set_id in output_dict:
                    metadata = output_dict[set_id]
                    for col, value in metadata.items():
                        if col in density_df.columns:
                            density_df.at[index, col] = str(value) if not pd.isna(value) else None
            
            density_df.to_csv(density_data_csv_path, index=False)
            return density_df
        except Exception as e:
            logging.error(f"Error updating metadata: {e}")
            return None

    def process_files_parallel(self, json_files, output_prefix, valid_set_ids=None):
        """Process multiple JSON files in parallel"""
        try:
            file_chunks = self._split_files(json_files, 10)
            with Pool(cpu_count()) as pool:
                pool.starmap(self.process_chunk, 
                    [(chunk, f'{output_prefix}{i}.csv', valid_set_ids) 
                     for i, chunk in enumerate(file_chunks)])
        except Exception as e:
            logging.error(f"Error in parallel processing: {e}")

    def _split_files(self, files, chunks):
        """Split files into chunks for parallel processing"""
        chunk_size = len(files) // chunks
        return [files[i:i + chunk_size] for i in range(0, len(files), chunk_size)]

    def standardize_columns(self):
        """Standardize column names in the dataset"""
        if self.data is not None:
            self.data.columns = [str(col).strip().lower() for col in self.data.columns]
            for old_col, new_col in self.column_mappings.items():
                if old_col in self.data.columns:
                    self.data.rename(columns={old_col: new_col}, inplace=True)
        return self
