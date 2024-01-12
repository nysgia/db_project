import sqlite3
import pandas as pd
import os
 
conn = sqlite3.connect('camping_org.db')
 
csv_directory = 'data_gen/'
 
csv_files = [f for f in os.listdir(csv_directory) if f.endswith('.csv')]
 
for csv_file in csv_files: 
    table_name = os.path.splitext(csv_file)[0]
 
    csv_file_path = os.path.join(csv_directory, csv_file)
    print(csv_file_path)
    open(csv_file_path, 'a').close()
 
    df = pd.read_csv(csv_file_path)
    df.columns = df.columns.str.strip()
 
    df.to_sql(table_name, conn, if_exists='replace', index=False)
 
conn.close()
