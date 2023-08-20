import random
import string

IGNORED_USER_FIELDS = ['id', 'password', 'groups', 'user_permissions', 'is_staff', 'is_superuser', 'last_login', 'is_active', 'date_joined', 'email']
IGNORED_DJANGO_ARGUMENTS = ['--verbosity', '--settings', '--pythonpath', '--traceback', '--no_color', '--force_color', '--skip_checks']

def available_arguments(options):
    argument_list = [f'--{key}' for key in options.keys()]
    argument_list = [argument for argument in argument_list if argument not in IGNORED_DJANGO_ARGUMENTS]
    return argument_list

def generate_password(length=8):
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for _ in range(length))
    return password
