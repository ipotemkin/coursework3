# import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from databases import Database


# def run_sql(sql: str):
#     con = sqlite3.connect("movies.db")
#     cur = con.cursor()
#     res = cur.execute(sql)
#     # res = [dict(*i) for i in res]
#     return res.fetchall()


def run_sql_alchemy(sql: str):
    engine = create_engine("sqlite:///movies.db")
    # session = sessionmaker(bind=engine)
    res = engine.execute(sql)
    return [dict(i) for i in res]


async def run_asql(sql: str):
    dbase = Database("sqlite:///movies.db")
    # dbase.connect()
    res = await dbase.fetch_all(query=sql)
    return res


async def get_one(sql: str):
    dbase = Database("sqlite:///movies.db")
    # dbase.connect()
    res = await dbase.fetch_one(query=sql)  # , values={"id": pk})
    return res



# sql = "select * from movie"
# print(run_sql(sql))
# # print(*[line for line in res], sep='\n')
#
# print([dict(i) for i in res])
# res = run_asql(sql)
# print(res)
