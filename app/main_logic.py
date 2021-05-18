from openpyxl import load_workbook
import pandas as pd
from app.calc import *
from app.maxmin import maximize, minimize

#создание пользовательского параметра 
def create_new_param(phrase, table, params, name, df):
	f_df = table.copy()
	our_df = df.copy()
	new_parameter = create_parameter(f_df, phrase, params)

	our_df = pd.concat([our_df, new_parameter], keys = ['Название', name], axis=1)

	return our_df


#Расчет рейтингов
def create_rate(weight, df):

	val_list = [] #список возвращаемых значений
	our_df = df.copy()
	formula = ''

	#Создание столбца "Рейтинг"
	rate = pd.Series([0 for i in range(0,len(weight))])
	rate.name = 'Рейтинг'

	#Расчет значений и конструирование части формулы
	for key, val in weight.items():
		rate += our_df[key]*val

		if formula:
			formula += '+'
		formula += key+ '*'+str(val)

	#нормализация
	rate *= 1000
	#присоединение столбца к общей таблице
	our_df = pd.concat([our_df, rate], axis=1)

	#перемещение столбца с рейтингами в начало

	column_list = list(our_df)
	column_list[1], column_list[-1] = column_list[-1], column_list[1]
	# our_df.columns = column_list
	our_df = our_df[column_list]
	#Генерация формулы
	formula = str(1000)+'*'+'('+formula+')'

	#Возврат значений из ф-ции
	val_list.append(our_df)
	val_list.append(formula)

	return val_list


def data_inp(filename):

	book = load_workbook(filename)
	sheet = book.worksheets[0]
	#data_frame = pd.DataFrame(sheet.values)
	data = sheet.values
	cols = next(data)
	#data_lst = list(data)
	data_frame = (pd.DataFrame(data, columns=cols))
	return data_frame

# the_big_table = 'test.xlsx'
# big_tbl = data_inp(the_big_table)

# #Формирование сырых показателей

# parameters = []

# for item in big_tbl.columns:
# 	if (item == 'Название'):
# 		flag = 1
# 	if flag == 1:
# 		parameters.append(item)

# parameters = parameters[1:] #выводятся пользователю для выбора

# our_df = big_tbl['Название']

# #создание пользовательского параметра 

# line = "<Параметр1> + <Параметр2> +3 * (<Параметр1> * <Параметр2>)" #то, что пользователь вводит - имитация
# new_parameter_name = 'Новый параметр'

# our_df = create_new_param(line, big_tbl, parameters, new_parameter_name, our_df)


# #Подготовка необходимой таблицы

# inp_list = ['Параметр1','Параметр2'] #то, что пользователь выбрал - имитация

# for i in range(0, len(inp_list)):

# 	our_df = pd.concat([our_df,big_tbl[inp_list[i]]], axis = 1)

# print(our_df) 

# #максимизация и минимизация

# par_for_max = 'Новый параметр' #имя параметра для максимизации - имитация

# our_df= maximize(our_df, par_for_max)

# print(our_df)

# par_for_min = 'Новый параметр' #имя параметра для миниимизации - имитация

# our_df = minimize(our_df, par_for_min)

# print(our_df)

# #Ввод весов
# weight = {'Параметр1':0.7, 'Новый параметр':0.2, 'Параметр2': 0.1} #то, что пользователь вводит - имитация

# #Расчет рейтингов
# example = create_rate(weight, our_df)

# our_df = example[0]

# print(our_df, '\n' ,example[1])

