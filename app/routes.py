import json
import os
from datetime import datetime

from flask import (
    render_template,
    redirect,
    url_for,
    request,
    session,
    send_from_directory,
)
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy import func
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename

from app import app, db
from app.forms import SignUpForm, SignInForm
from app.main_logic import *
from app.models import User, Params, Rate_formula


# Удаление файла из папки
def delete_file(file):
    file_for_del = os.path.join(app.config["FOLDER_FOR_FILES"], file)
    if os.path.isfile(file_for_del):
        os.remove(file_for_del)


# Проверка расширений
def legal_files(name):
    return "." in name and name.rsplit(".", 1)[1] in app.config["ALLOWED_FILES"]


# Приветствие
@app.route("/")
@app.route("/index")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("main"))
    return render_template("index.html")


# Личный кабинет
@app.route("/account")
@app.route("/account/<int:page>")
@login_required
def account(page=1):
    if current_user:
        user = db.session.query(User).get(current_user.get_id())
        rates = (
            db.session.query(Rate_formula)
            .filter_by(author_id=current_user.get_id())
            .paginate(page, app.config["POSTS_ON_PAGE"], False)
        )
    return render_template("lk.html", usr=user, rates=rates)


# Вход
@app.route("/signin", methods=["GET", "POST"])
def signin():
    error = ""
    # перенаправление авторизованного пользователя
    if current_user.is_authenticated:
        return redirect(url_for("main"))

    form = SignInForm()

    if form.validate_on_submit():  # проверка данных в форме
        user = User.query.filter_by(email=form.email.data).first()

        if user is None or not user.check_pass(form.password.data):
            error = "Неправильное имя пользователя или пароль"
            return render_template("signin.html", form=form, error_mes=error)

        # перенаправление уже зарегестрированного пользователя на главную страницу
        login_user(user)
        neccessary_page = request.args.get("next")
        if not neccessary_page or url_parse(neccessary_page).netloc != "":
            neccessary_page = url_for("main")
        return redirect(neccessary_page)

    return render_template("signin.html", form=form, error_mes=error)


# Регистрация
@app.route("/signup", methods=["GET", "POST"])  # добавить подтверждение по почте
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("main"))
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(name=form.name.data, email=form.email.data)
        user.create_pass_hash(form.password.data)
        db.session.add(user)
        db.session.commit()
        # flash('Пользователь успешно зарегестрирован')
        return redirect(url_for("signin"))
    return render_template("signup.html", form=form)


# Выход
@app.route("/exit")
def exit():
    logout_user()
    return redirect(url_for("index"))


# Главная страница
@app.route("/main")
@app.route("/main/<int:page>")
@login_required
def main(page=1):
    # при переходе на главную страницу
    # все ранее загруженные файлы удаляются
    del_file()
    if current_user:
        usr_id = current_user.get_id()

    lis_dir = os.listdir(app.config["FOLDER_FOR_FILES"])
    for item in lis_dir:
        if item.find("_" + usr_id + "_") != -1:
            os.remove(os.path.join(app.config["FOLDER_FOR_FILES"], item))

    # сброс флагов действий
    session["id_edit"] = -1  # флаг редактирования формулы
    session["id_build"] = -1  # флаг построения рейтинга по формуле

    authors = []

    ratings_lst = db.session.query(Rate_formula).paginate(
        page, app.config["POSTS_ON_PAGE"], False
    )

    return render_template("main.html", rates=ratings_lst)


# Загрузка файла на сервер
@app.route("/upload", methods=["GET", "POST"])  # TO DO:добавить проверку на пустой файл
@login_required
def save_file():
    error_empty_file = ""

    if request.method == "POST":
        dl_file = request.files.get("file")

        if dl_file and legal_files(dl_file.filename):
            f_name_list = dl_file.filename.rsplit(".", 1)

            if current_user:
                f_name = secure_filename(
                    f_name_list[0]
                    + "_"
                    + current_user.get_id()
                    + "_"
                    + datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                    + "."
                    + f_name_list[1]
                )

            f_path = os.path.join(app.config["FOLDER_FOR_FILES"], f_name)
            dl_file.save(f_path)

            book = load_workbook(f_path)
            sheet = book.worksheets[0]
            data = sheet.values

            if len(list(data)) == 0:
                error_empty_file = "Ошибка! Пустой файл."
                delete_file(f_name)
                return render_template("file_upload.html", error=error_empty_file)

            # замена знаков < и >
            big_tbl = data_inp(f_path)

            # замена пустых полей нулями
            big_tbl = big_tbl.replace(to_replace=np.nan, value=0)

            parameters = []

            for item in big_tbl.columns:
                if item:
                    if "<" in item:
                        item = item.replace("<", "")

                    if ">" in item:
                        item = item.replace(">", "")

                    parameters.append(item)
                else:
                    error_empty_file = "Ошибка! Пустой файл."
                    delete_file(f_name)
                    return render_template("file_upload.html", error=error_empty_file)

            big_tbl.columns = parameters

            big_tbl.to_excel(f_path, index=False)

            usr = db.session.query(User).get(current_user.get_id())

            # если в БД есть ссылка на файл, то удаляем её и файл (если существует)
            if usr.file_path:
                delete_file(usr.file_path)
                usr.file_path = ""
                db.session.commit()

            usr.file_path = f_name
            db.session.commit()

            # в зависимости от того, для чего загружается файл,
            # перенаправляем на другую страницу
            if session.get("id_build") != -1:
                return redirect("make_rate")
            else:
                return redirect(url_for("chooseparams"))
    return render_template("file_upload.html")


# Удаление файла
@app.route("/del_file")
@login_required
def del_file():
    if current_user:
        user = db.session.query(User).get(current_user.get_id())

    if user.file_path:
        delete_file(user.file_path)
        user.file_path = ""
        db.session.commit()

    return redirect(url_for("main"))


# Загрузка файла с сервера
@app.route("/download/<path:filename>")
@login_required
def dowload_file(filename):
    return send_from_directory(
        app.config["FOLDER_FOR_FILES"], app.config["FOLDER_FOR_FILES"] + "/" + filename
    )


# Выбор частных показателей
@app.route("/chooseparams", methods=["GET", "POST"])
@login_required
def chooseparams():
    error_no_param = ""

    # Если редактируем готовую формулу
    items = []
    if session.get("id_edit") != -1:
        f_items = []
        rate = db.session.query(Rate_formula).get(session.get("id_edit"))
        for el in rate.params:
            items.append(el.par_name)
            f_items.append(el.formula)

    if current_user:
        user = db.session.query(User).get(current_user.get_id())
    big_tbl = data_inp(os.path.join(app.config["FOLDER_FOR_FILES"], user.file_path))

    # Формирование сырых показателей

    parameters = []

    for item in big_tbl.columns:
        if item == "Название":
            flag = 1
        if flag == 1:
            parameters.append(item)

    parameters = parameters[1:]  # выводятся пользователю для выбора

    if request.method == "POST":

        data = request.json  # type - list

        if items:
            for i in range(0, len(data)):  # было от 1
                # если параметр уже создан, получаем инф-ю о нём из БД

                if data[i]["name"] in items:
                    data[i]["formula"] = f_items[items.index(data[i]["name"])]

        for i in range(0, len(data)):
            if data[i]["formula"] == "":
                if data[i]["name"] not in parameters:
                    error_no_param = (
                        "Ошибка! Нет параметра\n"
                        + data[i]["name"]
                        + ". Загрузите новый файл или выберите другие параметры"
                    )
                    return (
                        json.dumps({"error": True}),
                        404,
                        {"ContentType": "application/json"},
                    )
                # return render_template('error.html', error=error_no_param)
        # добавление в БД 1го параметра
        par = Params(formula=data[0]["formula"], par_name=data[0]["name"])
        db.session.add(par)
        db.session.commit()

        first_id = db.session.query(
            func.max(Params.id)
        ).scalar()  # начало диапазона созданных парметров

        # добавление в БД остальных параметров
        for i in range(1, len(data)):
            par = Params(formula=data[i]["formula"], par_name=data[i]["name"])
            db.session.add(par)
            db.session.commit()

        last_id = db.session.query(
            func.max(Params.id)
        ).scalar()  # конец диапазона созданных парметров

        session["first_id"] = first_id
        session["last_id"] = last_id

        # return redirect(url_for('finish'))
        return json.dumps({"success": True}), 200, {"ContentType": "application/json"}
    if items:
        return render_template(
            "params.html", table=parameters, addition=items, num=len(items)
        )
    else:
        return render_template("params.html", table=parameters, error=error_no_param)


# Присвоение весов показателям и создание формулы
@app.route("/finish", methods=["GET", "POST"])
@login_required
def finish():
    # диапазон необходимых параметров
    first_id = session.get("first_id")
    last_id = session.get("last_id") + 1

    if current_user:
        user = db.session.query(User).get(current_user.get_id())

    big_tbl = data_inp(os.path.join(app.config["FOLDER_FOR_FILES"], user.file_path))

    pars_names = []
    parametr = {}

    for i in range(first_id, last_id):
        par = db.session.query(Params).get(i)
        parametr["name"] = par.par_name

        if par.weight:
            parametr["weight"] = par.weight

        pars_names.append(parametr.copy())

    # добавление новой формулы в БД
    if request.method == "POST":

        data = request.json
        forml = Rate_formula(
            fl_name=data["rate_name"],
            author_id=current_user.get_id(),
            formula=data["rate_formula"],
        )
        db.session.add(forml)
        db.session.commit()

        # id последней созданной формулы
        fl_id = (
            db.session.query(Rate_formula)
            .filter_by(author_id=current_user.get_id())
            .order_by(Rate_formula.id.desc())
            .first()
            .id
        )

        # связь формулы и параметров
        for i in range(first_id, last_id):
            temp = db.session.query(Params).get(i)
            temp.rating_id = fl_id
            db.session.commit()

        dic_w = data["data"]

        # присвоение весов
        for key, value in dic_w.items():
            paramtr = (
                db.session.query(Params)
                .filter_by(rating_id=fl_id, par_name=key)
                .first()
            )
            paramtr.weight = value
            db.session.commit()

        paramtr = ""
        flags = data["flags"]

        # присвоение флагов максимизации/минимизации
        for key, value in flags.items():

            paramtr = (
                db.session.query(Params)
                .filter_by(rating_id=fl_id, par_name=key)
                .first()
            )

            if 1 in value:
                if [i for i, arr in enumerate(value) if 1 == arr][0] == 0:
                    paramtr.flag_max = 1

                elif [i for i, arr in enumerate(value) if 1 == arr][0] == 1:
                    paramtr.flag_min = 1

            db.session.commit()

        # return redirect(url_for('make_rate'))

    return render_template("params_table.html", params=pars_names, len=len(pars_names))


# Расчтёт рейтинга
@app.route("/make_rate")
@login_required
def make_rate():
    error = ""
    if current_user:
        user = db.session.query(User).get(current_user.get_id())

    big_tbl = data_inp(os.path.join(app.config["FOLDER_FOR_FILES"], user.file_path))

    # Если считается по готовой формуле
    if session.get("id_build") != -1:
        fl = db.session.query(Rate_formula).get(session.get("id_build"))
    else:
        # выбор последней созданной формулы
        fl = (
            db.session.query(Rate_formula)
            .filter_by(author_id=current_user.get_id())
            .order_by(Rate_formula.id.desc())
            .first()
        )

    # Формирование сырых показателей

    parameters = []

    for item in big_tbl.columns:
        if item == "Название":
            flag = 1

        if flag == 1:
            parameters.append(item)

    parameters = parameters[1:]

    our_df = big_tbl["Название"]
    inp_list = []
    weight_list = {}

    # проверка
    if session.get("id_build") != -1:
        for param in fl.params:
            if param.formula == "":
                if param.par_name not in parameters:
                    return render_template(
                        "error.html",
                        error="Ошибка! В файле отсутствуют нужные показатели",
                    )

    # создание пользовательского параметра

    for item in fl.params:
        weight_list[item.par_name] = item.weight

        if item.formula:

            our_df = create_new_param(
                item.formula, big_tbl, parameters, item.par_name, our_df
            )

            if type(our_df) == str:
                error = our_df
                return render_template("error.html", error=error)
        else:
            inp_list.append(item.par_name)

    for i in range(0, len(inp_list)):
        our_df = pd.concat([our_df, big_tbl[inp_list[i]]], axis=1)

    # максимизация/минимизация параметров
    for item in fl.params:
        if item.flag_max == 1:
            our_df = maximize(our_df, item.par_name)
        elif item.flag_min == 1:
            our_df = minimize(our_df, item.par_name)

    # расчёт рейтинга
    example = create_rate(weight_list, our_df)
    our_df = example[0]
    our_df = our_df.sort_values(by="Рейтинг", ascending=False)
    our_df.index = sorted(our_df.index.values.tolist())
    our_df = our_df.round(3)
    # print(our_df, '\n' ,example[1])

    # export to xlsx
    if current_user:
        f_name = (
            "example"
            + "_"
            + current_user.get_id()
            + "_"
            + datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            + ".xlsx"
        )

    f_path = os.path.join(app.config["FOLDER_FOR_FILES"], f_name)
    writer = pd.ExcelWriter(os.path.join(f_path), engine="xlsxwriter")
    our_df.to_excel(writer, "Sheet1")
    writer.save()

    return render_template("rating.html", table=our_df, formula=example[1], file=f_name)


# Изменение формулы
@app.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    # Обработка кнопки
    if request.method == "POST":
        data = int(request.json)
        session["id_edit"] = data
    return json.dumps({"success": True}), 200, {"ContentType": "application/json"}


# Построение рейтинга по формуле
@app.route("/build", methods=["GET", "POST"])
@login_required
def build():
    # Обработка кнопки
    if request.method == "POST":
        data = int(request.json)
        session["id_build"] = data
    return json.dumps({"success": True}), 200, {"ContentType": "application/json"}


# Удаление формулы
@app.route("/del_rate", methods=["GET", "POST"])
@login_required
def del_rate():
    if request.method == "POST":
        data = int(request.json)
        post = db.session.query(Rate_formula).get(data)
        db.session.delete(post)
        db.session.commit()
        return json.dumps({"success": True}), 200, {"ContentType": "application/json"}


@app.route("/error")
@login_required
def error():
    return render_template("error.html")
