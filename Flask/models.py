# coding: utf-8
from sqlalchemy import Column, Float, Integer, Table, Text
from sqlalchemy.sql.sqltypes import NullType
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class BOX(db.Model):
    __tablename__ = 'BOX'

    id = db.Column(db.Integer, primary_key=True)
    movie_key = db.Column(db.Integer, nullable=False)
    kor_title = db.Column(db.Text, nullable=False)
    aud_num = db.Column(db.Integer)


class NVactor(db.Model):
    __tablename__ = 'NVactor'

    id = db.Column(db.Integer, primary_key=True)
    movie_key = db.Column(db.Integer, nullable=False)
    act_img = db.Column(db.Text)
    staff_act = db.Column(db.Text)
    act_role = db.Column(db.Text)


class NVmovie(db.Model):
    __tablename__ = 'NVmovie'

    id = db.Column(db.Integer, primary_key=True)
    title_kor = db.Column(db.Text, nullable=False)
    title_eng = db.Column(db.Text, nullable=False)
    score_aui = db.Column(db.Float)
    score_cri = db.Column(db.Float)
    score_net = db.Column(db.Float)
    poster = db.Column(db.Text)
    genre = db.Column(db.Text)
    country = db.Column(db.Text)
    runtime = db.Column(db.Text)
    opendate = db.Column(db.Text)
    film_rate = db.Column(db.Text)
    summary = db.Column(db.Text)
    story = db.Column(db.Text)
    prod_img = db.Column(db.Text)
    staff_prod = db.Column(db.Text)
    len_quotes = db.Column(db.Integer)


class NVquote(db.Model):
    __tablename__ = 'NVquotes'

    id = db.Column(db.Integer, primary_key=True)
    movie_key = db.Column(db.Integer, nullable=False)
    quote = db.Column(db.Text)
    actor = db.Column(db.Text)
    role = db.Column(db.Text)
    real_quote = db.Column(db.Text)
    isreal = db.Column(db.Integer, nullable=False)


class NVrecoMovie(db.Model):
    __tablename__ = 'NVreco_movie'

    id = db.Column(db.Integer, primary_key=True)
    movie_key = db.Column(db.Integer, nullable=False)
    reco_title = db.Column(db.Text)
    reco_url = db.Column(db.Text)


class REALQUOTE(db.Model):
    __tablename__ = 'REALQUOTE'

    id = db.Column(db.Integer, primary_key=True)
    movie_key = db.Column(db.Integer, nullable=False)
    subtitle_key = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.Integer, nullable=False)
    lines = db.Column(db.Text, nullable=False)
    h_index = db.Column(db.Integer, nullable=False)


class REALQUOTES(db.Model):
    __tablename__ = 'REALQUOTE2'

    id = db.Column(db.Integer, primary_key=True)
    movie_key = db.Column(db.Integer, nullable=False)
    subtitle_key = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.Integer, nullable=False)
    lines = db.Column(db.Text)
    g_index = db.Column(db.Integer)


class Subtitle(db.Model):
    __tablename__ = 'Subtitles'

    id = db.Column(db.Integer, primary_key=True)
    movie_key = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.Text, nullable=False)
    lines = db.Column(db.Text, nullable=False)
    is_real = db.Column(db.Integer)


class Subtitles2(db.Model):
    __tablename__ = 'Subtitles2'

    id = db.Column(db.Integer, primary_key=True)
    movie_key = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.Text, nullable=False)
    lines = db.Column(db.Text, nullable=False)
    is_real = db.Column(db.Integer)

#
# t_sqlite_sequence = db.Table(
#     'sqlite_sequence',
#     db.Column('name', db.NullType),
#     db.Column('seq', db.NullType)
# )
