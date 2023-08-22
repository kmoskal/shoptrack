import random
import string

IGNORED_USER_FIELDS = ['id', 'password', 'groups', 'user_permissions', 'is_staff', 'is_superuser', 'last_login', 'is_active', 'date_joined', 'email']

IGNORED_DJANGO_ARGUMENTS = ['--verbosity', '--settings', '--pythonpath', '--traceback', '--no_color', '--force_color', '--skip_checks']

DISTRICT = [
    'Białystok', 'Bielsko-Biała', 'Elbląg', 'Gdańsk', 'Gdynia', 'Kalisz',
    'Katowice', 'Kołobrzeg', 'Konin', 'Koszalin', 'Kraków', 'Lublin',
    'Łomża', 'Łódź', 'Opole', 'Ostrowiec Świętokrzyski', 'Oświęcim', 
    'Piotrków Trybunalski', 'Płock', 'Poznań', 'Pruszków', 'Radom',
    'Rybnik', 'Siedlce', 'Sosnowiec', 'Suwałki', 'Szczecin', 'Toruń',
    'Warszawa-Wschód', 'Warszawa-Zachód', 'Zamość'
]

REGION = ['Centrum', 'Południe', 'Północ', 'Wschód', 'Zachód']

def available_arguments(options):
    argument_list = [f'--{key}' for key in options.keys()]
    argument_list = [argument for argument in argument_list if argument not in IGNORED_DJANGO_ARGUMENTS]
    return argument_list

def generate_password(length=8):
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def validate_shop_id(shop_id):
    ''' Shop ID must have the first two characters and the last three digits. e.g. "FA001".'''
    if shop_id[:2].isalpha() and shop_id[2:].isdigit() and len(shop_id) == 5:
        return True
    else:
        return False
