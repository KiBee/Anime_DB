import sqlalchemy
import pandas as pd


class Db:

    def __init__(self, bd_name):
        self.bd_name = bd_name
        self.engine = self.connect()

    def connect(self):
        mysql_engine = f'mysql://root@localhost:3306/{self.bd_name}?charset=utf8'
        engine = sqlalchemy.create_engine(mysql_engine)
        return engine

    def show_all(self):
        q = """
                SHOW TABLES
            """
        return pd.read_sql(q, con=self.engine)

    def show_table(self, table_name):
        q = f"""
                SELECT *
                FROM {table_name}
            """
        return pd.read_sql(q, con=self.engine)

    def clear_table(self, table_name):
        q = f"""
                DELETE
                FROM {table_name}
            """

        self.engine.execute(q)
        print(table_name, 'cleaned')

    def join(self, l_table, r_table, l_col, r_col, l_show, r_show, type_join, header=True):
        if type(l_table) == pd.DataFrame:
            print('nonono')
            return

        q = f"""
                SELECT {l_table}.{l_show}, {r_table}.{r_show}
                FROM {l_table} {type_join} JOIN {r_table}
                ON {l_table}.{l_col} = {r_table}.{r_col}
                
            """
        return pd.read_sql(q, con=self.engine)

    def staging_left_join(self, l_table, st_table, r_table, l_col, r_col, l_show, r_show):
        q = f"""
                SELECT {l_table}.{l_show}, {r_table}.{r_show}
                FROM {l_table} 
                LEFT JOIN {st_table}
                ON {l_table}.{l_col} = {st_table}.{l_col}
                LEFT JOIN {r_table}
                ON {r_table}.{r_col} = {st_table}.{r_col}
            """
        return pd.read_sql(q, con=self.engine)

    def describe(self, table_name):
        q = f"""
                DESCRIBE {table_name}
            """
        print(q)
        return pd.read_sql(q, con=self.engine)
