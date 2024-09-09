import pandas as pd
import glob


csv_files = glob.glob("../data/new/*.csv")
dataframes = [pd.read_csv(file) for file in csv_files]

merged_df = pd.concat(dataframes, ignore_index=True)

merged_df.to_csv("merged_disasters.csv", index=False)