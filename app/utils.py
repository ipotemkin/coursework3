from sqlalchemy import create_engine
from databases import Database


def run_sql_alchemy(sql: str):
    engine = create_engine("sqlite:///movies.db")
    res = engine.execute(sql)
    return [dict(i) for i in res]


async def run_asql(sql: str):
    dbase = Database("sqlite:///movies.db")
    res = await dbase.fetch_all(query=sql)
    return res


async def get_one(sql: str):
    dbase = Database("sqlite:///movies.db")
    res = await dbase.fetch_one(query=sql)  # , values={"id": pk})
    return res
