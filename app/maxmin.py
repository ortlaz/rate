# from openpyxl import load_workbook
# import pandas as pd


def maximize(df, param):
	f_df = df.copy()
	max_el = f_df[param].max()
	min_el = f_df[param].min()

	for ind in range(0,len(f_df[param])):
		f_df.loc[ind, param] = (f_df[param][ind] - min_el)/(max_el-min_el)

	return f_df


def minimize(df, param):
	f_df = df.copy()
	max_el = f_df[param].max()
	min_el = f_df[param].min()

	for ind in range(0,len(f_df[param])):
		f_df.loc[ind, param] = (max_el-f_df[param][ind] )/(max_el-min_el)

	return f_df


# def data_inp(filename):

# 	book = load_workbook(filename)
# 	sheet = book.worksheets[0]
# 	#data_frame = pd.DataFrame(sheet.values)
# 	data = sheet.values
# 	cols = next(data)
# 	#data_lst = list(data)
# 	data_frame = (pd.DataFrame(data, columns=cols))
# 	return data_frame


# the_big_table = 'test.xlsx'
# big_tbl = data_inp(the_big_table)

# name = 'Параметр2' #имя параметра для максимизации или минимизации

# big_tbl = maximize(big_tbl, name)

# print(big_tbl)

# big_tbl = minimize(big_tbl, name)

# print(big_tbl)
