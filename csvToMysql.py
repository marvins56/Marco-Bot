import os
import mysql.connector
import pandas as pd
from sqlalchemy import create_engine

def create_database(database_name):
    cnx = mysql.connector.connect(
        host='localhost',
        user='root',
        password='password'
    )

    cursor = cnx.cursor()
    cursor.execute(f"CREATE DATABASE {database_name}")
    cursor.close()

    cnx.database = database_name
    return cnx

def insert_csv_data(cnx, csv_directory):
    for file in os.listdir(csv_directory):
        if file.endswith(".csv"):
            table_name = os.path.splitext(file)[0]  # Use the filename without extension as table name
            file_path = os.path.join(csv_directory, file)
            df = pd.read_csv(file_path)
            
            engine = create_engine('mysql+mysqlconnector://root:password@localhost/macrol')
            df.head(0).to_sql(name=table_name, con=engine, if_exists='replace', index=False)
            df.to_sql(name=table_name, con=engine, if_exists='append', index=False)

def main():
    # Replace 'macrol' with the name of your new database
    database_name = 'macrol'
    
    # Replace 'C:/Users/jukas/Desktop/Mackro/makroldb/marcodb' with the path to your directory containing the CSV files
    csv_directory = 'C:/Users/jukas/Desktop/Mackro/makroldb/marcodb'
    
    cnx = create_database(database_name)
    insert_csv_data(cnx, csv_directory)
    cnx.close()

if __name__ == "__main__":
    main()
