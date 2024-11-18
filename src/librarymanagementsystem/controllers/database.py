import os

import mysql.connector as connection
import pandas as pd
import sqlalchemy
from dotenv import load_dotenv

load_dotenv()


class Database:
    def __init__(self):
        self.host = os.getenv("HOST")
        self.database = os.getenv("DATABASE")
        self.user = os.getenv("USER")
        self.password = os.getenv("PASSWORD")

    def getEngine(self) -> sqlalchemy.engine.base.Connection:
        connection_string = f"mysql+pymysql://{self.user}:{self.password if self.password is not None else ""}@{self.host}/{self.database}"
        return sqlalchemy.create_engine(connection_string, echo=False)

    def getConnection(self) -> connection.MySQLConnection:
        return connection.connect(
            host=self.host,
            database=self.database,
            user=self.user,
            password=self.password,
            use_pure=True,
        )

    def exec_query(self, query: str) -> pd.DataFrame:
        try:
            engine = self.getEngine()
            with engine.connect() as conn:
                result = conn.execute(sqlalchemy.text(query))
                columns = result.keys()
                data = result.fetchall()

                result_dataFrame = pd.DataFrame(data, columns=columns)

                return result_dataFrame
        except Exception as e:
            print("Failed to read table {}".format(e))

    def exec_query_with_commit(self, query: str):
        try:
            engine = self.getEngine()
            with engine.connect() as conn:
                result = conn.execute(sqlalchemy.text(query))
                conn.commit()  # Save the changes to the database
                print(
                    result.rowcount, "Enregistrement modifié avec succès dans la table"
                )
        except Exception as e:
            print("Erreur lors de l'exécution de la requête {}".format(e))
