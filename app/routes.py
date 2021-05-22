from flask import render_template, flash, redirect, url_for, request, session
from app import app, db
from app.forms import SignUpForm, SignInForm
from app.models import User, Params, Rate_formula
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
import os, json
from datetime import datetime
from app.main_logic import *
from sqlalchemy import func
from tzlocal import get_localzone

def delete_file(file):
		file_for_del = os.path.join(app.config['FOLDER_FOR_FILES'], file)
		if os.path.isfile(file_for_del):
			os.remove(file_for_del)


def legal_files(name):
	return '.' in name and name.rsplit('.', 1)[1] in app.config['ALLOWED_FILES']

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
	if current_user.is_authenticated:
		return redirect(url_for('main'))
	form = SignInForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is None or not user.check_pass(form.password.data):
			flash('Неправильное имя пользователя или пароль')
			return redirect(url_for('signin'))
		login_user(user)
		neccessary_page = request.args.get('next')
		if not neccessary_page or url_parse(neccessary_page).netloc != '':
			neccessary_page = url_for('main')
		return redirect(neccessary_page)
	return render_template('signin.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
	if current_user.is_authenticated:
		return redirect(url_for('main'))
	form = SignUpForm()
	if form.validate_on_submit():
		user = User(name=form.name.data, email=form.email.data)
		user.create_pass_hash(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Пользователь успешно зарегестрирован')
		return redirect(url_for('signin'))
	return render_template('signup.html', form=form)

@app.route('/exit')
def exit():
	logout_user()
	return redirect(url_for('index'))

@app.route('/main')
@login_required
def  main():
	session['id_edit'] = -1
	session['id_build'] = -1
	names = []
	formulas = []
	authors = []
	time = []
	ids = []
	ratings_lst = db.session.query(Rate_formula).all()
	for item in ratings_lst:
		names.append(item.fl_name)
		formulas.append(item.formula)
		authors.append(db.session.query(User).get(item.author_id).name)
		time.append(item.time.strftime("%d.%m.%y"))
		ids.append(item.id)
	n = len(ratings_lst)

	return render_template('main.html',ids=ids, names = names, formulas=formulas, authors=authors, time=time, n=n)


@app.route('/upload', methods=['GET', 'POST'])  #TO DO:добавить проверку на пустой файл
@login_required
def save_file():

	print(session.get('id_edit'))
	print(session.get('id_build'))

	if request.method == 'POST':
		dl_file = request.files.get('file')

		if dl_file and legal_files(dl_file.filename):
			f_name_list = dl_file.filename.rsplit('.',1)
			if current_user:
				f_name = secure_filename(f_name_list[0]+'_'+current_user.get_id()+'_'+datetime.now().strftime("%Y-%m-%d_%H-%M-%S") +'.'+f_name_list[1])
			f_path = os.path.join(app.config['FOLDER_FOR_FILES'], f_name)
			dl_file.save(f_path)

			usr = db.session.query(User).get(current_user.get_id())
			if usr.file_path:
				delete_file(usr.file_path);
				usr.file_path = ''
				db.session.commit()
			usr.file_path = f_name
			db.session.commit()

			if session.get('id_build') != -1:
				return redirect('make_rate')
			else:
				return redirect(url_for('chooseparams'))
	return render_template('file_upload.html')

@app.route('/chooseparams', methods=['GET', 'POST'])
@login_required
def chooseparams():

	# print(session.get('id_edit'))
	# print(session.get('id_build'))
	
	if session.get('id_edit') != -1:
		items = []
		f_items = []
		rate = db.session.query(Rate_formula).get(session.get('id_edit'))
		for el in rate.params:
			if el.formula:
				items.append(el.par_name)
				f_items.append(el.formula)


	if current_user:
		user = db.session.query(User).get(current_user.get_id())
	big_tbl = data_inp(os.path.join(app.config['FOLDER_FOR_FILES'], user.file_path))
	#Формирование сырых показателей

	parameters = []

	for item in big_tbl.columns:
		if (item == 'Название'):
			flag = 1
		if flag == 1:
			parameters.append(item)

	parameters = parameters[1:] #выводятся пользователю для выбора

	if request.method == "POST":
		data = request.json #type - list

		if items:
			for i in range(1,len(data)):
				if data[i]['name'] in items:
					par = Params(formula = f_items[items.index(data[i]['name'])], par_name = data[i]['name'])
					db.session.add(par)
					db.session.commit()
					data.remove(data[i])					

		par = Params(formula = data[0]['formula'], par_name = data[0]['name'])
		db.session.add(par)
		db.session.commit()
		first_id = db.session.query(func.max(Params.id)).scalar()
		for i in range(1,len(data)):
			par = Params(formula = data[i]['formula'], par_name = data[i]['name'])
			db.session.add(par)
			db.session.commit()	
		last_id = db.session.query(func.max(Params.id)).scalar()
		session['first_id'] = first_id
		session['last_id'] = last_id
		
		# return redirect(url_for('finish'))
		return json.dumps({'success':True}),200,{'ContentType':'application/json'}

	return render_template('params.html', table = parameters, addition=items, num=len(items))

@app.route('/finish', methods=['GET', 'POST'])
@login_required
def finish():
	first_id = session.get('first_id')
	last_id = session.get('last_id') + 1
	if current_user:
		user = db.session.query(User).get(current_user.get_id())
	big_tbl = data_inp(os.path.join(app.config['FOLDER_FOR_FILES'], user.file_path))
	# params = []
	pars_names = []
	parametr = {}
	for i in range(first_id, last_id):
		par = db.session.query(Params).get(i)
		# params.append(par)
		parametr['name']=par.par_name
		if par.weight:
			parametr['weight']=par.weight
		pars_names.append(parametr.copy())

	if request.method == "POST":
		data = request.json
		forml = Rate_formula(fl_name = data['rate_name'], author_id = current_user.get_id(), formula=data['rate_formula'])
		db.session.add(forml)
		db.session.commit()


		fl_id = db.session.query(Rate_formula).filter_by(author_id=current_user.get_id()).order_by(Rate_formula.id.desc()).first().id

		for i in range(first_id, last_id):
			temp = db.session.query(Params).get(i)
			temp.rating_id = fl_id
			db.session.commit()

		dic_w = data['data']

		for key,value in dic_w.items():

			paramtr = db.session.query(Params).filter_by(rating_id = fl_id, par_name=key).first()
			paramtr.weight = value
			db.session.commit()


		paramtr = ''
		flags = data['flags']

		for key,value in flags.items():

			paramtr = db.session.query(Params).filter_by(rating_id = fl_id, par_name=key).first()

			if 1 in value:
				if [i for i, arr in enumerate(value) if 1 == arr][0] == 0:
					paramtr.flag_max = 1

				elif [i for i, arr in enumerate(value) if 1 == arr][0] == 1:
					paramtr.flag_min = 1

			db.session.commit()

			# return redirect(url_for('make_rate'))

	return render_template('params_table.html', params = pars_names, len=len(pars_names))

@app.route('/del_file')
@login_required
def del_file():
	if current_user:
		user = db.session.query(User).get(current_user.get_id())
	if user.file_path:
		delete_file(user.file_path);
		user.file_path = ''
		db.session.commit()
	return redirect(url_for('main'))

@app.route('/make_rate')
@login_required
def make_rate():
	if current_user:
		user = db.session.query(User).get(current_user.get_id())
	big_tbl = data_inp(os.path.join(app.config['FOLDER_FOR_FILES'], user.file_path))
	if session.get('id_build'):
		fl = db.session.query(Rate_formula).get(session.get('id_build'))
		print(fl)
	else:
		fl = db.session.query(Rate_formula).filter_by(author_id=current_user.get_id()).order_by(Rate_formula.id.desc()).first()

		#Формирование сырых показателей

	parameters = []

	for item in big_tbl.columns:
		if (item == 'Название'):
			flag = 1
		if flag == 1:
			parameters.append(item)

	parameters = parameters[1:] 

	our_df = big_tbl['Название']
	inp_list = []
	weight_list = {}

	#создание пользовательского параметра
	for item in fl.params:
		weight_list[item.par_name]=item.weight
		if item.formula:
			our_df = create_new_param(item.formula, big_tbl, parameters, item.par_name, our_df)
		else:
			inp_list.append(item.par_name)

	for i in range(0, len(inp_list)):
		our_df = pd.concat([our_df,big_tbl[inp_list[i]]], axis = 1)
	
	for item in fl.params:
		if item.flag_max == 1:
			our_df = maximize(our_df, item.par_name)
		elif item.flag_min == 1:
			our_df = minimize(our_df, item.par_name)

	example = create_rate(weight_list, our_df)
	our_df = example[0]
	our_df.round(3)
	our_df = our_df.sort_values(by='Рейтинг', ascending=False)
	our_df.index = sorted(our_df.index.values.tolist())
	# print(our_df, '\n' ,example[1])

	return render_template('rating.html', table = our_df, formula=example[1])

@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
	if request.method == "POST":
		data = int(request.json)
		session['id_edit'] = data
	return json.dumps({'success':True}),200,{'ContentType':'application/json'}

@app.route('/build', methods=['GET', 'POST'])
@login_required
def build():
	if request.method == "POST":
		data = int(request.json)
		session['id_build'] = data
	return json.dumps({'success':True}),200,{'ContentType':'application/json'}

