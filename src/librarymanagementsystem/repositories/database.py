import os

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
            print("Erreur lors de la lecture de la table {}".format(e))
            return pd.DataFrame([], columns=[])

    def exec_query_with_commit(self, query: str):
        try:
            engine = self.getEngine()
            with engine.connect() as conn:
                result = conn.execute(sqlalchemy.text(query))
                conn.commit()
                print(
                    result.rowcount, "Enregistrement modifié avec succès dans la table"
                )
        except Exception as e:
            print("Erreur lors de l'exécution de la requête {}".format(e))

    def exec_queries_with_commit(self, queries: list[str]):
        try:
            engine = self.getEngine()
            with engine.connect() as conn:
                for query in queries:
                    conn.execute(sqlalchemy.text(query))
                conn.commit()
                print("Enregistrement modifié avec succès dans la table")
        except Exception as e:
            print("Erreur lors de l'exécution de la requête {}".format(e))
