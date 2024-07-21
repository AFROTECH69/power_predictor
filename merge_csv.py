import pandas as pd
import glob

class CSVCombiner:
    def __init__(self, input_dir, output_file):
        self.input_dir = input_dir
        self.output_file = output_file
    
    def concatenate_csv(self):
        # Use glob to find all CSV files in the input directory
        all_files = glob.glob(self.input_dir + "/*.csv")
        
        # Initialize an empty list to store dataframes
        df_list = []
        
        # Iterate over all CSV files and read each one into a pandas DataFrame
        for filename in all_files:
            df = pd.read_csv(filename, index_col=None, header=0)
            df_list.append(df)
        
        # Concatenate all dataframes into a single dataframe
        combined_df = pd.concat(df_list, axis=0, ignore_index=True)
        
        # Write the combined dataframe to a single CSV file
        combined_df.to_csv(self.output_file, index=False)
        
        print(f'Combined CSV file saved as {self.output_file}')



input_directory = 'data'
output_file = 'combined_output.csv'

# Create an instance of CSVCombiner
combiner = CSVCombiner(input_directory, output_file)

# Call the concatenate_csv method to combine CSV files
combiner.concatenate_csv()