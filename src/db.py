from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
import pandas as pd

DRIVER = "ODBC Driver 18 for SQL Server"
SERVIDOR = "D07S22-1252907\SQLEXPRESSART"
BANCO = "HamburgueriaBrasa"


def conectar():
    odbc = (
        f"DRIVER={{{DRIVER}}};"
        f"SERVER={SERVIDOR};"
        f"DATABASE={BANCO};"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
    )

    return create_engine(
        "mssql+pyodbc:///?odbc_connect=" + quote_plus(odbc)
    )


def consultar(sql):
    with conectar().connect() as conexao:
        return pd.read_sql(text(sql), conexao)


def mensagem_erro(erro):
    """Tira só a mensagem do SQL Server do meio do texto do erro."""
    achou = re.search(r"\[SQL Server\](.+?)\s*\(\d+\)", str(erro))
    return achou.group(1) if achou else str(erro)