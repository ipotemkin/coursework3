import time

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from uvicorn import run

from app.utils import get_one
from app.errors import NotFoundError, NoContentError, ValidationError, DatabaseError, BadRequestError
from app.views import directors, genres, movies, users, auth, tokens, favorites
from databases import Database

from app.dependencies import del_expired_tokens
from fastapi_utils.tasks import repeat_every
import datetime

from fastapi.middleware.cors import CORSMiddleware

tags_metadata = [
    {
        'name': 'movies',
        'description': 'Операции с фильмами',
    },
    {
        'name': 'directors',
        'description': 'Операции с режиссерами',
    },
    {
        'name': 'genres',
        'description': 'Операции с жанрами',
    },
    {
        'name': 'users',
        'description': 'Операции с пользователями',
    },
    {
        'name': 'auth',
        'description': 'Операции с токенами',
    },
    {
        'name': 'aio',
        'description': 'Асинхронные операции с базой (тест)',
    },
    {
        'name': 'tokens',
        'description': 'Операции с базой токенов (тест)',
    },
    {
        'name': 'favorites',
        'description': 'Операции с записями юзер–любимый фильм (тест)',
    },
    # {
    #     'name': 'docs',
    #     'description': 'Документация',
    # },
]


app = FastAPI(title='Movies API on FastAPI',
              description='This is a refactored app from lessons 18 and 19',
              version='1.0.0',
              openapi_tags=tags_metadata,
              docs_url='/')

origins = [
    # "http://domainname.com",
    # "https://domainname.com",
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(movies.router)
app.include_router(directors.router)
app.include_router(genres.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(tokens.router)
app.include_router(favorites.router)


@app.on_event("startup")
@repeat_every(seconds=60*60*24)
def del_expired_tokens_repeat():
    del_expired_tokens()
    print('Expired tokens deleted', datetime.datetime.utcnow())  # TODO: remove this debug on release


@app.on_event("startup")
def on_startup():
    pass
    # init_db()
    #
    # print("app's items:", app.__dict__)  # TODO: remove on release


# exception handlers
@app.exception_handler(404)
@app.exception_handler(NotFoundError)
def not_found_error(request: Request, exc: NotFoundError):
    return JSONResponse(
        status_code=404,
        content={'message': "Not Found"}
    )


@app.exception_handler(NoContentError)
def no_content_error(request: Request, exc: NoContentError):
    return JSONResponse(
        status_code=204,
        content={'message': "No Content"}
    )


@app.exception_handler(DatabaseError)
def database_error(request: Request, exc: DatabaseError):
    return JSONResponse(
        status_code=400,
        content={'message': "Database Error"}
    )


@app.exception_handler(BadRequestError)
def bad_request_error(request: Request, exc: BadRequestError):
    return JSONResponse(
        status_code=400,
        content={'message': "Bad Request"}
    )


@app.exception_handler(ValidationError)
def validation_error(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=400,
        content={'message': "Validation Error"}
    )


@app.get('/aio/directors', tags=['aio'])
async def aio_directors_get_all():
    """
    Получить всех режиссеров
    """
    dbase = Database("sqlite:///movies.db")
    t0 = time.perf_counter()
    # res = await run_asql('select * from director')
    res = await dbase.fetch_all(query='select * from director')
    elapsed = time.perf_counter() - t0
    print('aio with databases [%0.8fs]' % elapsed)
    return res


@app.get('/aio/directors/{pk}', tags=['aio'])
async def aio_directors_get_one(pk: int):
    """
    Получить режиссера по ID
    """
    return await get_one(f'select * from director where id = {pk} limit 1')


if __name__ == '__main__':
    run(
        "run:app",
        host='localhost',
        port=8000,
        reload=True
    )
