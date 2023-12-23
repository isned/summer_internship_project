'''from sqlalchemy import create_engine
import pandas as pd

class DataAccess:
    def __init__(self):
        db_url = "mysql+mysqlconnector://root:root@localhost:3306/data"
        self.engine = create_engine(db_url)

    def get_customer_data(self):
        data = pd.read_sql("SELECT * FROM Customers", self.engine)
        return data'''
from sqlalchemy import create_engine
import pandas as pd

class DataAccess:
    def __init__(self):
        db_url = "mysql+mysqlconnector://root:root@localhost:3306/data"
        self.engine = create_engine(db_url)

    def get_customer_data(self, user_id):
        query = f"SELECT * FROM customers WHERE customer_id = {user_id}"
        data = pd.read_sql(query, self.engine)
        return data

