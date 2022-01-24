from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse

from uvicorn import run

from app.errors import NotFoundError, NoContentError, ValidationError, DatabaseError, BadRequestError
from app.views import directors, genres, movies, users, auth, favorites, genre

from app.dependencies import del_expired_tokens
from fastapi_utils.tasks import repeat_every
import datetime

from fastapi.middleware.cors import CORSMiddleware

from app.constants import RATE_LIMIT_PER_SECOND, NO_RATE_LIMIT

from app.setup_db import TESTING

# rate limitation
import aioredis
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter

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
        'name': 'favorites',
        'description': 'Операции с любимыми фильмами',
    },
]

app = FastAPI(title='Movies API on FastAPI',
              description='Coursework Module 3 with SkyPro',
              version='1.0.0',
              contact={
                  "name": "Igor Potemkin",
                  "email": "ipotemkin@rambler.ru",
              },
              openapi_tags=tags_metadata,
              docs_url='/',
              dependencies=[Depends(RateLimiter(times=RATE_LIMIT_PER_SECOND, seconds=1))] if not TESTING and not NO_RATE_LIMIT else None
              )

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
app.include_router(favorites.router)
app.include_router(genre.router)


@app.on_event("startup")
@repeat_every(seconds=60*60*24)
def del_expired_tokens_repeat():
    del_expired_tokens()
    print('Expired tokens deleted', datetime.datetime.utcnow())


@app.on_event("startup")
async def on_startup():
    if not NO_RATE_LIMIT:
        redis = aioredis.from_url("redis://localhost")  # , encoding="utf-8", decode_responses=True)
        # create_redis_pool("redis://localhost")  # ths string from the manual doesn't work
        await FastAPILimiter.init(redis)
    print(NO_RATE_LIMIT)


@app.on_event("shutdown")
async def on_shutdown():
    if not NO_RATE_LIMIT:
        await FastAPILimiter.close()


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


if __name__ == '__main__':
    run(
        "run:app",
        host='localhost',
        port=8000,
        reload=True
    )
