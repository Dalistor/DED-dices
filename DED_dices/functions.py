from django.contrib.auth.models import User

#validar conta de usuário
def userVerify(username, email, password, password_confirm):
	is_valid = True
	error_message = None

	if username == '':
		is_valid = False
		error_message = 'Nome de usuário inválido'

	elif User.objects.filter(username=username).exists():
		is_valid = False
		error_message = 'Nome de usuário já existe'

	elif User.objects.filter(email=email).exists():
		is_valid = False
		error_message = 'Email já cadastrado'

	elif password != password_confirm:
		is_valid = False
		error_message = 'Senhas não correspondem'

	elif password == '':
		is_valid = False
		error_message = 'Senha inválida'	

	return {
		'is_valid': is_valid,
		'error_message': error_message
	}

class GS():
	getter = None
	setter = None