import dask.dataframe as dd
from sqlalchemy import create_engine

engine = create_engine('sqlite:///C:/Users/abiji/Desktop/project-root/database.db')
ddf = dd.read_csv('data/health_data.csv', assume_missing=True)
pdf = ddf.compute()
table_name = 'health_statistics' 
pdf.to_sql(table_name, engine, if_exists='replace', index=False)
print(f'Data from {table_name} has been written to the database successfully!')
