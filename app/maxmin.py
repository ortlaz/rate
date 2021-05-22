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



