import pandas as pd
import datetime
from sqlalchemy import create_engine

def execute():
	engine = create_engine("postgresql://")

	# csv read
	csv_file = ""
	df = pd.read_csv(csv_file)

	df['starttime'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

	# db insert
	with engine.begin() as conn:
		df.to_sql(name='jira_ticketing', con=conn, if_exists='append', index=False)
       
if __name__ == "__main__":
    df = execute() 
        