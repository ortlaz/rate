from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy.orm import synonym


@login.user_loader
def get_user(id):
    return User.query.get(int(id))


# Таблица Пользователей


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(200), index=True)
    file_path = db.Column(db.String(200))
    rates = db.relationship("Rate_formula", backref="author_", lazy="dynamic")

    # def __repr__(self):
    #     return '<User {}>'.format(self.username)

    # def __init__(self, id, email, password_hash, name, file_path):
    # 	self.id = id
    # 	self.email = email
    # 	self.password_hash = password_hash
    # 	self.name = name
    # 	self.file_path = file_path

    # шифрование пароля
    def create_pass_hash(self, password):
        self.password_hash = generate_password_hash(password)

    # проверка паролей
    def check_pass(self, password):
        return check_password_hash(self.password_hash, password)


# Таблица Формул Рейтингов


class Rate_formula(db.Model):
    __tablename__ = "formulas"
    id = db.Column(db.Integer, primary_key=True)
    fl_name = db.Column(db.String(200), index=True)
    formula = db.Column(db.String(1024))
    time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    params = db.relationship("Params", backref="rating_", lazy="dynamic")

    # def __init__(self, id, f_name, time):
    # 	self.id = id
    # 	self.fl_name = f_name
    # 	self.time = time


# Таблица Параметра


class Params(db.Model):
    __tablename__ = "parameters"
    id = db.Column(db.Integer, primary_key=True)
    formula = db.Column(db.String(1024))
    weight = db.Column(db.Float)
    par_name = db.Column(db.String(200), index=True)
    flag_max = db.Column(db.Integer)
    flag_min = db.Column(db.Integer)  # 1, если надо максимизировать/инимизировать
    rating_id = db.Column(db.Integer, db.ForeignKey("formulas.id"))

    # def __init__(self, id, formula, weight,par_name,flag_min,flag_max):
    # 	self.id = id
    # 	self.formula = formula
    # 	self.weight = weight
    # 	self.par_name = par_name
    # 	self.flag_max = flag_max
    # 	self.flag_min = flag_min
