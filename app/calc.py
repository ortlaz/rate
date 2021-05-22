import operator

OPERS = {'+': (1, operator.add), '-': (1, operator.sub),
         '*': (2, operator.mul), '/': (2, operator.truediv),
         '^': (3, operator.pow)}


def create_parameter(df, line, lst):

	#парсинг введённой строки
	def str_parser(strin):

		parameter = ''

		if (strin.count('<') != strin.count('>') or strin.count('(') != strin.count(')')):
		    print("Error") #сделать нормальный вывод ошибки

		else:
		    i = k = 0

		    while i < len(strin):

		    	#Собираем название показателя
		        if strin[i] == "<" and parameter == '':
		            i += 1
		            k = i
		            while strin[k] != ">":
		                parameter += strin[k]
		                k += 1
		            i=k

		        #Собираем число
		        if strin[i] in "0123456789.":
		            parameter += strin[i]

		        #Вывод того, что собрали
		        elif parameter:
		            yield parameter
		            parameter = ''

		        #Если символ - оператор
		        if strin[i] in OPERS or strin[i] in "()":
		            yield strin[i]

		        i += 1
		        
		    #Вывод последнего значения в строке    
		    if parameter:
		            yield parameter

	
	#Инфиксная польская запись
	def ppz(parsed):

		stack = []

		for element in parsed:

			if element in OPERS:

				while stack and stack[-1] != "(" and OPERS[element][0] <= OPERS[stack[-1]][0]:
					yield stack.pop()
				
				stack.append(element)

			elif element == ")": 

				while stack:
					a = stack.pop()

					if a == "(":
						break

					yield a

			
			elif element == "(":
				stack.append(element)

			else:
				yield element


		while stack:
			yield stack.pop()

	#Подсчет значений
	def result(ppz_str):

		stack = []

		for el in ppz_str:

			if el in OPERS:

				b, a = stack.pop(), stack.pop()

				#Если верхние элементы строки, то преобразуем их
				if type(a) == str and type(b) == str:

					if a.isdigit():
						a = float(a)
						
					elif a in df.columns:
						a = df[a]
					else:
						return('no parameter')

					if b.isdigit():
						b = float(b)

					elif b in df.columns:
						b = df[b]
					else:
						return('no parameter')

					#Нельзя складывать и вычитать столбей со скаляром
					if (el == '+' or el == '-') and type(a) != type (b):
						return('Error')  #сделать нормальный вывод ошибки

				#Преобразуем скаляр
				elif type(a) == str:
					if a.isdigit():
						a = float(a)
					elif a in df.columns:
						a = df[a]
					

				elif type(b) == str:
					if b.isdigit():
						b = float(b)
					elif b in df.columns:
						b = df[b]

				stack.append(OPERS[el][1](a, b))
					
			else:
				stack.append(el)

		return stack[0]
		            
	return result(ppz(str_parser(line)))

