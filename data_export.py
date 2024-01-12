import sqlite3
import csv
import os
 
conn = sqlite3.connect("camping_org.db")
cursor = conn.cursor()
 
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
table_names = [table[0] for table in cursor.fetchall()]
 
csv_directory = "data_gen/"
 
for table_name in table_names: 
    cursor.execute(f"SELECT * FROM {table_name};")
    data = cursor.fetchall()
 
    cursor.execute(f"PRAGMA table_info({table_name});")
    column_names = [column[1] for column in cursor.fetchall()]
 
    csv_file_path = os.path.join(csv_directory, f"{table_name}.csv")
 
    with open(csv_file_path, mode="w", newline="", encoding="utf-8") as csv_file:
        csv_writer = csv.writer(csv_file)
         
        csv_writer.writerow(column_names)
 
        csv_writer.writerows(data)

print("CSV files updated successfully.") 
conn.close()
