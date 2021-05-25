import os

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'M00nL1ghT'
	SQLALCHEMY_TRACK_MODIFICATIONS = False #отключение оповещений об ошибках в БД
	SQLALCHEMY_DATABASE_URI = 'postgresql://root:laibach@localhost:5432/ratings' #URL БД
	FOLDER_FOR_FILES = '/home/stasy/rate/app/uploads'
	ALLOWED_FILES = set(['xlsx', 'xlsm'])
	POSTS_ON_PAGE = 5