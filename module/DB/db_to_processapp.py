import pandas as pd
from sqlalchemy import create_engine

def execute():
    engine = create_engine("postgresql://")
    
    df = pd.read_sql("SELCET * FROM jira_ticketing", con=engine)
    
    return df

if __name__ == "__main__":
    df = execute()