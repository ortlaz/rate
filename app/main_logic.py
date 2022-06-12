from openpyxl import load_workbook
import pandas as pd
from app.calc import *
from app.maxmin import maximize, minimize

# создание пользовательского параметра
def create_new_param(phrase, table, params, name, df):
    f_df = table.copy()
    our_df = df.copy()
    new_parameter = create_parameter(f_df, phrase, params)

    if type(new_parameter) == str:
        # если вернулась ошибка
        return new_parameter

    # Проверка деления на 0 для столбцов
    new_parameter = new_parameter.replace((np.inf, -np.inf), (None, None))

    for el in new_parameter.isnull():
        if el == True:
            return "Ошибка! деление на 0"
        else:
            our_df = pd.concat([our_df, new_parameter], keys=["Название", name], axis=1)
            return our_df


# Расчет рейтингов
def create_rate(weight, df):

    val_list = []  # список возвращаемых значений
    our_df = df.copy()
    formula = ""

    # Создание столбца "Рейтинг"
    rate = pd.Series([0 for i in range(0, len(our_df.index))])
    rate.name = "Рейтинг"

    # Расчет значений и конструирование части формулы

    for key, val in weight.items():

        rate += our_df[key] * val

        if formula:
            formula += "+"
        formula += key + "*" + str(val)

    # нормализация
    rate *= 1000

    # присоединение столбца к общей таблице
    our_df = pd.concat([our_df, rate], axis=1)

    # перемещение столбца с рейтингами в начало
    column_list = list(our_df)
    column_list[1], column_list[-1] = column_list[-1], column_list[1]
    our_df = our_df[column_list]

    # Генерация формулы
    formula = str(1000) + "*" + "(" + formula + ")"

    # Возврат значений из ф-ции
    val_list.append(our_df)
    val_list.append(formula)

    return val_list


def data_inp(filename):

    book = load_workbook(filename)
    sheet = book.worksheets[0]
    data = sheet.values
    cols = next(data)
    data_frame = pd.DataFrame(data, columns=cols)
    return data_frame
