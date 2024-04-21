import pandas as pd
import sqlite3

# data = pd.read_csv("movies.csv")[["Title", "Rating", "Year", "Summary", "YouTube Trailer"]]
# conn = sqlite3.connect('films.db')
# data.to_sql('Films', conn, if_exists='replace', index=False)
# conn.close()

class DBSelecter():

    def __init__(self, db_name):
        self.db_name = db_name

    def select(self, query):
        conn = sqlite3.connect(self.db_name)
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    
    def fetch_one(self, query, target_type):
        conn = sqlite3.connect(self.db_name)
        df = pd.read_sql_query(query, conn)
        conn.close()

        return target_type(df.values[0][0])