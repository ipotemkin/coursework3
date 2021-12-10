import os
from http import HTTPStatus
import pytest
from app.dao.model.movies import Movie
from fixtures import data
from run import app
from fastapi.testclient import TestClient
from app.constants import ITEMS_ON_PAGE

client = TestClient(app)


test_movie_request = {
    "description": "Владелец ранчо пытается сохранить землю своих предков. Кевин Костнер в неовестерне от автора «Ветреной реки»",
    "director_id": 1,
    "genre_id": 17,
    "rating": 8.6,
    "title": "Йеллоустоун",
    "trailer": "https://www.youtube.com/watch?v=UKei_d0cbP4",
    "year": 2018,
    "id": 100,
}


test_movie_response = {
    "description": "Владелец ранчо пытается сохранить землю своих предков. Кевин Костнер в неовестерне от автора «Ветреной реки»",
    "director_id": 1,
    "genre_id": 17,
    "rating": 8.6,
    "title": "Йеллоустоун",
    "trailer": "https://www.youtube.com/watch?v=UKei_d0cbP4",
    "year": 2018,
    "id": 100,
    "director": {
        "id": 1,
        "name": "Тейлор Шеридан"
    },
    "genre": {
        "id": 17,
        "name": "Вестерн"
    }
}

test_movies_response = [
    {
        "description": "Владелец ранчо пытается сохранить землю своих предков. Кевин Костнер в неовестерне от автора «Ветреной реки»",
        "director_id": 1,
        "genre_id": 17,
        "rating": 8.6,
        "title": "Йеллоустоун",
        "trailer": "https://www.youtube.com/watch?v=UKei_d0cbP4",
        "year": 2018,
        "id": 1,
        "director": {
            "id": 1,
            "name": "Тейлор Шеридан"
        },
        "genre": {
            "id": 17,
            "name": "Вестерн"
        }
    },
    {
        "description": "США после Гражданской войны. Легендарный охотник за головами Джон Рут по кличке Вешатель конвоирует заключенную. По пути к ним прибиваются еще несколько путешественников. Снежная буря вынуждает компанию искать укрытие в лавке на отшибе, где уже расположилось весьма пестрое общество: генерал конфедератов, мексиканец, ковбой… И один из них - не тот, за кого себя выдает.",
        "director_id": 2,
        "genre_id": 4,
        "rating": 7.8,
        "title": "Омерзительная восьмерка",
        "trailer": "https://www.youtube.com/watch?v=lmB9VWm0okU",
        "year": 2015,
        "id": 2,
        "director": {
            "id": 2,
            "name": "Квентин Тарантино"
        },
        "genre": {
            "id": 4,
            "name": "Драма"
        }
    },
    {
        "description": "События происходят в конце XIX века на Диком Западе, в Америке. В основе сюжета — сложные перипетии жизни работяги — старателя Габриэля Конроя. Найдя нефть на своем участке, он познает и счастье, и разочарование, и опасность, и отчаяние...",
        "director_id": 3,
        "genre_id": 17,
        "rating": 6,
        "title": "Вооружен и очень опасен",
        "trailer": "https://www.youtube.com/watch?v=hLA5631F-jo",
        "year": 1978,
        "id": 3,
        "director": {
            "id": 3,
            "name": "Владимир Вайншток"
        },
        "genre": {
            "id": 17,
            "name": "Вестерн"
        }
    },
    {
        "description": "Эксцентричный охотник за головами, также известный как Дантист, промышляет отстрелом самых опасных преступников. Работенка пыльная, и без надежного помощника ему не обойтись. Но как найти такого и желательно не очень дорогого? Освобождённый им раб по имени Джанго – прекрасная кандидатура. Правда, у нового помощника свои мотивы – кое с чем надо сперва разобраться.",
        "director_id": 2,
        "genre_id": 17,
        "rating": 8.4,
        "title": "Джанго освобожденный",
        "trailer": "https://www.youtube.com/watch?v=2Dty-zwcPv4",
        "year": 2012,
        "id": 4,
        "director": {
            "id": 2,
            "name": "Квентин Тарантино"
        },
        "genre": {
            "id": 17,
            "name": "Вестерн"
        }
    },
    {
        "description": "История превращения застенчивого парня Реджинальда Дуайта, талантливого музыканта из маленького городка, в суперзвезду и культовую фигуру мировой поп-музыки Элтона Джона.",
        "director_id": 4,
        "genre_id": 18,
        "rating": 7.3,
        "title": "Рокетмен",
        "trailer": "https://youtu.be/VISiqVeKTq8",
        "year": 2019,
        "id": 5,
        "director": {
            "id": 4,
            "name": "Декстер Флетчер"
        },
        "genre": {
            "id": 18,
            "name": "Мюзикл"
        }
    },
    {
        "description": "Али - молодая амбициозная девушка из маленького городка с чудесным голосом, совсем недавно потеряла своих родителей. Теперь никому не нужная, она отправляется в большой город Лос-Анджелес, где устраивается на работу у Тесс, хозяйки ночного клуба «Бурлеск». За короткое время она находит друзей, поклонников и любовь всей своей жизни. Но может ли сказка длиться вечно? Ведь немало людей завидует этой прекрасной танцовщице...",
        "director_id": 5,
        "genre_id": 18,
        "rating": 6.4,
        "title": "Бурлеск",
        "trailer": "https://www.youtube.com/watch?v=sgOhxneHkiE",
        "year": 2010,
        "id": 6,
        "director": {
            "id": 5,
            "name": "Стив Энтин"
        },
        "genre": {
            "id": 18,
            "name": "Мюзикл"
        }
    },
    {
        "description": "Рокси Харт мечтает о песнях и танцах и о том, как сравняться с самой Велмой Келли, примадонной водевиля. И Рокси действительно оказывается с Велмой в одном положении, когда несколько очень неправильных шагов приводят обеих на скамью подсудимых.",
        "director_id": 6,
        "genre_id": 18,
        "rating": 7.2,
        "title": "Чикаго",
        "trailer": "https://www.youtube.com/watch?v=YxzS_LzWdG8",
        "year": 2002,
        "id": 7,
        "director": {
            "id": 6,
            "name": "Роб Маршалл"
        },
        "genre": {
            "id": 18,
            "name": "Мюзикл"
        }
    },
    {
        "description": "Париж, 1899 год. Знаменитый ночной клуб «Мулен Руж» — это не только дискотека и шикарный бордель, но и место, где, повинуясь неудержимому желанию прочувствовать атмосферу праздника, собираются страждущие приобщиться к красоте, свободе, любви и готовые платить за это наличными.",
        "director_id": 7,
        "genre_id": 18,
        "rating": 7.6,
        "title": "Мулен Руж",
        "trailer": "https://www.youtube.com/watch?v=lpiMCTd87gE",
        "year": 2001,
        "id": 8,
        "director": {
            "id": 7,
            "name": "Баз Лурман"
        },
        "genre": {
            "id": 18,
            "name": "Мюзикл"
        }
    },
    {
        "description": "Эндрю мечтает стать великим. Казалось бы, вот-вот его мечта осуществится. Юношу замечает настоящий гений, дирижер лучшего в стране оркестра. Желание Эндрю добиться успеха быстро становится одержимостью, а безжалостный наставник продолжает подталкивать его все дальше и дальше – за пределы человеческих возможностей. Кто выйдет победителем из этой схватки?",
        "director_id": 8,
        "genre_id": 4,
        "rating": 8.5,
        "title": "Одержимость",
        "trailer": "https://www.youtube.com/watch?v=Q9PxDPOo1jw",
        "year": 2013,
        "id": 9,
        "director": {
            "id": 8,
            "name": "Дэмьен Шазелл"
        },
        "genre": {
            "id": 4,
            "name": "Драма"
        }
    },
    {
        "description": "Авторитетный взгляд на историю культового электронного стиля глазами самых известных его представителей и последователей. Увлекательный рассказ о феномене итало-диско и возможность увидеть своими глазами, что творилось на главных танцполах 80-х.",
        "director_id": 9,
        "genre_id": 9,
        "rating": 0,
        "title": "Наследие итало-диско",
        "trailer": "https://www.youtube.com/watch?v=LVdRR6m5OdQ",
        "year": 2017,
        "id": 10,
        "director": {
            "id": 9,
            "name": "Пьетро Антон"
        },
        "genre": {
            "id": 9,
            "name": "Документальное"
        }
    },
    {
        "description": "Юность певца Джонни Кэша была омрачена гибелью его брата и пренебрежительным отношением отца. Военную службу будущий певец проходил в Германии. После свадьбы и рождения дочери он выпустил свой первый хит и вскоре отправился в турне по США вместе с Джерри Ли Льюисом, Элвисом Пресли и Джун Картер, о которой он безнадёжно мечтал целых десять лет.",
        "director_id": 10,
        "genre_id": 4,
        "rating": 7.8,
        "title": "Переступить черту",
        "trailer": "https://www.youtube.com/watch?v=RnFrrzg1OEQ",
        "year": 2005,
        "id": 11,
        "director": {
            "id": 10,
            "name": "Джеймс Мэнголд"
        },
        "genre": {
            "id": 4,
            "name": "Драма"
        }
    },
    {
        "description": "Наследник знаменитого дома Атрейдесов Пол отправляется вместе с семьей на одну из самых опасных планет во Вселенной — Арракис. Здесь нет ничего, кроме песка, палящего солнца, гигантских чудовищ и основной причины межгалактических конфликтов — невероятно ценного ресурса, который называется меланж. В результате захвата власти Пол вынужден бежать и скрываться, и это становится началом его эпического путешествия. Враждебный мир Арракиса приготовил для него множество тяжелых испытаний, но только тот, кто готов взглянуть в глаза своему страху, достоин стать избранным.",
        "director_id": 11,
        "genre_id": 7,
        "rating": 8.4,
        "title": "Дюна",
        "trailer": "https://www.youtube.com/watch?v=DOlTmIhEsg0",
        "year": 2021,
        "id": 12,
        "director": {
            "id": 11,
            "name": "Дени Вильнёв"
        },
        "genre": {
            "id": 7,
            "name": "Фантастика"
        }
    },
    {
        "description": "Это история любви старлетки, которая между прослушиваниями подает кофе состоявшимся кинозвездам, и фанатичного джазового музыканта, вынужденного подрабатывать в заштатных барах. Но пришедший к влюбленным успех начинает подтачивать их отношения.",
        "director_id": 8,
        "genre_id": 18,
        "rating": 8,
        "title": "Ла-Ла Ленд",
        "trailer": "https://www.youtube.com/watch?v=lneNCBIXD4I",
        "year": 2016,
        "id": 13,
        "director": {
            "id": 8,
            "name": "Дэмьен Шазелл"
        },
        "genre": {
            "id": 18,
            "name": "Мюзикл"
        }
    },
    {
        "description": "Рассказ о начале творческого пути Виктора Цоя и группы «Кино», о его взаимоотношениях с Майком Науменко, его женой Натальей и многими, кто был в авангарде рок-движения Ленинграда 1981 года.",
        "director_id": 12,
        "genre_id": 4,
        "rating": 7.3,
        "title": "Лето",
        "trailer": "https://www.youtube.com/watch?v=TvAbtsQKrHA",
        "year": 2018,
        "id": 14,
        "director": {
            "id": 12,
            "name": "Кирилл Серебренников"
        },
        "genre": {
            "id": 4,
            "name": "Драма"
        }
    },
    {
        "description": "Джек Торренс с женой и сыном приезжает в элегантный отдалённый отель, чтобы работать смотрителем во время мертвого сезона. Торренс здесь раньше никогда не бывал. Или это не совсем так? Ответ лежит во мраке, сотканном из преступного кошмара.",
        "director_id": 14,
        "genre_id": 6,
        "rating": 8.4,
        "title": "Сияние ",
        "trailer": "https://www.youtube.com/watch?v=NMSUEhDWXH0",
        "year": 1980,
        "id": 15,
        "director": {
            "id": 14,
            "name": "Стэнли Кубрик"
        },
        "genre": {
            "id": 6,
            "name": "Триллер"
        }
    },
    {
        "description": "Что если в один прекрасный день в тебя вселяется существо-симбиот, которое наделяет тебя сверхчеловеческими способностями? Вот только Веном – симбиот совсем недобрый, и договориться с ним невозможно. Хотя нужно ли договариваться?.. Ведь в какой-то момент ты понимаешь, что быть плохим вовсе не так уж и плохо. Так даже веселее. В мире и так слишком много супергероев! Мы – Веном!",
        "director_id": 13,
        "genre_id": 7,
        "rating": 6.7,
        "title": "Веном",
        "trailer": "https://www.youtube.com/watch?v=n7GlLxV_Igk",
        "year": 2018,
        "id": 16,
        "director": {
            "id": 13,
            "name": "Рубен Фляйшер"
        },
        "genre": {
            "id": 7,
            "name": "Фантастика"
        }
    },
    {
        "description": "К своим 16 годам старшеклассник Донни уже знает, что такое смерть. После несчастного случая, едва не стоившего ему жизни, Донни открывает в себе способности изменять время и судьбу. Произошедшие с ним перемены пугают его окружение — родителей, сестер, учителей, друзей и любимую девушку.",
        "director_id": 15,
        "genre_id": 7,
        "rating": 8,
        "title": "Донни Дарко",
        "trailer": "https://www.youtube.com/watch?v=9H_t5cdszFU",
        "year": 2001,
        "id": 17,
        "director": {
            "id": 15,
            "name": "Ричард Келли"
        },
        "genre": {
            "id": 7,
            "name": "Фантастика"
        }
    },
    {
        "description": "Уже немолодой школьный учитель музыки Джо Гарднер всю жизнь мечтал выступать на сцене в составе джазового ансамбля. Однажды он успешно проходит прослушивание у легендарной саксофонистки и, возвращаясь домой вне себя от счастья, падает в люк и умирает. Теперь у Джо одна дорога — в Великое После, но он сбегает с идущего в вечность эскалатора и случайно попадает в Великое До. Тут новенькие души обретают себя, и у будущих людей зарождаются увлечения, мечты и интересы. Джо становится наставником упрямой души 22, которая уже много веков не может найти свою искру и отправиться на Землю.",
        "director_id": 16,
        "genre_id": 16,
        "rating": 8.1,
        "title": "Душа",
        "trailer": "https://www.youtube.com/watch?v=vsb8762mE6Q",
        "year": 2020,
        "id": 18,
        "director": {
            "id": 16,
            "name": "Пит Доктер"
        },
        "genre": {
            "id": 16,
            "name": "Мультфильм"
        }
    },
    {
        "description": "Париж. 1910 год. Ужасный монстр, напоминающий гигантское насекомое, нагоняет страх на всю Францию. Застенчивый киномеханик и неутомимый изобретатель начинают охоту на него. В этой погоне они знакомятся со звездой кабаре, сумасшедшим ученым и его умной обезьянкой и, наконец, самим монстром, который оказывается совсем не страшным. Теперь безобидное, как блоха, чудовище ищет у своих новых друзей защиты от вредного начальника городской полиции.",
        "director_id": 18,
        "genre_id": 16,
        "rating": 6.1,
        "title": "Монстр в Париже",
        "trailer": "https://www.youtube.com/watch?v=rKsdTuvrF5w",
        "year": 2010,
        "id": 19,
        "director": {
            "id": 18,
            "name": "Бибо Бержерон"
        },
        "genre": {
            "id": 16,
            "name": "Мультфильм"
        }
    },
    {
        "description": "От Великого потопа зверей спас ковчег. Но спустя полгода скитаний они готовы сбежать с него куда угодно. Нервы на пределе. Хищники готовы забыть про запреты и заглядываются на травоядных. Единственное спасение — найти райский остров. Там простор и полно еды. Но даже если он совсем близко, будут ли рады местные такому количеству гостей?",
        "director_id": 19,
        "genre_id": 16,
        "rating": 5.9,
        "title": "Упс... Приплыли!",
        "trailer": "https://www.youtube.com/watch?v=Qjpmysz4x-4",
        "year": 2020,
        "id": 20,
        "director": {
            "id": 19,
            "name": "Тоби Генкель"
        },
        "genre": {
            "id": 16,
            "name": "Мультфильм"
        }
    }
]


class TestMoviesView:
    @pytest.fixture
    def movies(self, db_session):
        for i in data['movies']:
            db_session.add(Movie(**i))
            db_session.commit()
        return data['movies']

    @pytest.fixture
    def new_movie(self, db_session):
        obj = Movie(**test_movie_request)
        db_session.add(obj)
        db_session.commit()
        return obj

    def test_testing_is_true(self):
        assert os.environ.get("TESTING") == 'TRUE'

    def test_many(self, db_session, movies):
        response = client.get("/movies/")
        assert response.status_code == HTTPStatus.OK
        assert response.json() == test_movies_response

    def test_many_with_page(self):
        response = client.get("/movies/?page=1")
        assert response.status_code == HTTPStatus.OK
        assert response.json() == test_movies_response[:ITEMS_ON_PAGE]

    def test_one(self, db_session):
        response = client.get("/movies/1")
        assert response.status_code == HTTPStatus.OK
        assert response.json() == test_movies_response[0]

    def test_one_not_found(self, db_session):
        response = client.get("/movies/1000")
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json() == {'message': 'Not Found'}

    # TODO: to make tests with tokens
    # def test_update(self, new_movie, db_session):
    #     response = client.patch("/movies/100", json=test_movie_request)
    #     assert response.status_code == HTTPStatus.OK
    #     assert response.json() == test_movie_response

    # def test_create(self, db_session):
    #     new_movie = {"id": 101, "name": "Новый жанр"}
    #     response = client.post("/movies", json=new_movie)
    #     assert response.status_code == HTTPStatus.CREATED
    #     assert response.json() == {"id": 101, "name": "Новый жанр"}
    #
    # def test_delete(self, db_session):
    #     response = client.delete("/movies/100")
    #     assert response.status_code == HTTPStatus.OK
    #     response = client.get("/movies/100")
    #     assert response.status_code == HTTPStatus.NOT_FOUND
