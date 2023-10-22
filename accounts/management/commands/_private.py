import random
import string
from accounts.models import User, Shop

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

def get_validate_employee_id():
    ''' Employee ID must contain Shop ID then "." and five digits. e.g. "FA001.00001" '''
    while True:
        employee_id = input('Enter employee ID: ').strip().upper()
        if employee_id == 'Q':
            return None
        elif employee_id[:2].isalpha() and employee_id[5] == '.' and employee_id[6:].isdigit():
            return employee_id
        else:
            raise ValueError('Employee ID must contain Shop ID then "." and five digits. e.g. "FA001.00001"')

def search_user(object):
    while True:
        email = input("Enter the user's email or press 'q' to quit: ").strip()
        if email == 'q':
            break
        try:
            user: User = User.objects.get(email=email)
            answer = input(f'Do you want to choose {user.username}? Confirm(Y/N)').strip().lower()
            if answer == 'y':
                user_to_assign: User = user
                return user_to_assign
            elif answer == 'n':
                continue
        except:
            object.stdout.write(object.style.ERROR(f'User with email "{email}" does not exist'))
            return None


def search_shop(object):
    while True:
        shop_id = input("Enter shop ID or press 'q' to quit: ").strip().upper()
        if shop_id == 'Q':
            break
        try:
            shop = Shop.objects.get(shop_id=shop_id)
            answer = input(f'Do you want to choose {shop.shop_id}? Confirm(Y/N)').strip().lower()
            if answer == 'y':
                return shop
            elif answer == 'n':
                continue

        except Shop.DoesNotExist:
            object.stdout.write(object.style.ERROR(f'Shop with {shop_id} does not exist.'))
            return None
