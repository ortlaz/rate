import unittest

import pandas as pd

import app.routes
from app import app, db
from app.main_logic import data_inp, create_new_param, create_rate
from app.maxmin import maximize
from app.models import User


class Tests(unittest.TestCase):
    def setUp(self):
        app.app.config['TESTING'] = True
        app.app.config['CRSF_ENABLED'] = False
        app.app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://root:laibach@localhost:5432/ratings_tests"
        self.app = app.app.test_client()
        db.create_all()

    def tearDown(self):
        db.session()
        db.drop_all()

    def test_user(self):
        usr = User(email='testuser@mail.ru')
        usr.create_pass_hash('password')
        self.assertTrue(usr.check_pass('password'))
        self.assertFalse(usr.check_pass('pass'))

    def test_data_inp(self):
        filename = 'testfiles/test.xlsx'
        result = data_inp(filename)
        etalon = pd.DataFrame([{'Название': 'аоа', 'Параметр1': 1.0, 'Параметр2': 32.0},
                               {'Название': 'оао', 'Параметр1': 5.6, 'Параметр2': 656.0},
                               {'Название': 'ооо', 'Параметр1': 7.0, 'Параметр2': 7.8}])
        self.assertTrue(result.equals(etalon))

    def test_create_new_param(self):
        filename = 'testfiles/tet2.xlsx'
        big_tbl = data_inp(filename)
        parameters = []
        for item in big_tbl.columns:
            if item:
                if '<' in item:
                    item = item.replace('<', '')
                if '>' in item:
                    item = item.replace('>', '')
            parameters.append(item)
        big_tbl.columns = parameters
        our_df = big_tbl['Название']

        error_null = 'Ошибка! деление на 0'
        error_form = 'Нельзя выполнять сложение или вычитание числа с целым столбцом'
        error_no_param = 'Нет параметра '

        self.assertTrue(create_new_param('<ф>/<в>*8', big_tbl, parameters, 'Новый параметр', our_df), error_null)
        etalon = pd.DataFrame([{'Название': 'вар', 'ж': (9.0)}, {'Название': 'авр', 'ж': 41.0},
                               {'Название': 'вара', 'ж': 5.0}, {'Название': 'рвр', 'ж': 44.0},
                               {'Название': 'пв', 'ж': 9.0}])
        result = create_new_param('<б>+<в>*8', big_tbl, parameters, 'ж', our_df)
        self.assertTrue(result.equals(etalon))
        self.assertTrue(create_new_param('<ф>+8', big_tbl, parameters, 'Новый параметр', our_df), error_form)
        self.assertTrue(create_new_param('8-<ф>', big_tbl, parameters, 'Новый параметр', our_df), error_form)
        self.assertTrue(create_new_param('<ф>+<t>', big_tbl, parameters, 'Новый параметр', our_df),
                        error_no_param + 't')

    def test_create_rate(self):
        filename = 'testfiles/test.xlsx'
        big_tbl = data_inp(filename)
        parameters = []
        for item in big_tbl.columns:
            if item:
                if '<' in item:
                    item = item.replace('<', '')
                if '>' in item:
                    item = item.replace('>', '')
            parameters.append(item)
        big_tbl.columns = parameters
        our_df = big_tbl['Название']

        weight = {'Параметр1': 0.7, 'Параметр2': 0.1}  # то, что пользователь вводит - имитация
        inp_list = ['Параметр1', 'Параметр2']
        for i in range(0, len(inp_list)):
            our_df = pd.concat([our_df, big_tbl[inp_list[i]]], axis=1)

        result = create_rate(weight, our_df)

        etalon = pd.DataFrame([{'Название': 'аоа', 'Рейтинг': 3900.0, 'Параметр2': 32.0, 'Параметр1': 1.0},
                               {'Название': 'оао', 'Рейтинг': 69520.0, 'Параметр2': 656.0, 'Параметр1': 5.6},
                               {'Название': 'ооо', 'Рейтинг': 5680.0, 'Параметр2': 7.8, 'Параметр1': 7.0}])
        self.assertTrue(result[0].round(1).equals(etalon))

    def test_maximize(self):
        filename = 'testfiles/test.xlsx'
        big_tbl = data_inp(filename)
        etalon = pd.DataFrame([{'Название': 'аоа', 'Параметр1': 0.00, 'Параметр2': 32.0},
                               {'Название': 'оао', 'Параметр1': 0.77, 'Параметр2': 656.0},
                               {'Название': 'ооо', 'Параметр1': 1.00, 'Параметр2': 7.8}])

        max_df = maximize(big_tbl, 'Параметр1')
        self.assertTrue(max_df.round(2).equals(etalon))

    def test_minimize(self):
        filename = 'testfiles/test.xlsx'
        big_tbl = data_inp(filename)
        etalon = pd.DataFrame([{'Название': 'аоа', 'Параметр1': 1.0, 'Параметр2': 0.04},
                               {'Название': 'оао', 'Параметр1': 5.6, 'Параметр2': 1.00},
                               {'Название': 'ооо', 'Параметр1': 7.0, 'Параметр2': 0.00}])

        min_df = maximize(big_tbl, 'Параметр2')
        self.assertTrue(min_df.round(2).equals(etalon))


if __name__ == '__main__':
    unittest.main()
