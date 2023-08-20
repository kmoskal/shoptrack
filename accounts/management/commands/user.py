from django.core.management.base import BaseCommand
from django.core.validators import validate_email
from django.utils.ipv6 import ValidationError 
from accounts.models import User
from accounts.management.commands._private import IGNORED_USER_FIELDS, available_arguments, generate_password


class Command(BaseCommand):
    help = 'Create a new user or edit an existing user'

    def add_arguments(self, parser):
        parser.add_argument('--add', action='store_true', help='Add a new user')
        parser.add_argument('--edit', action='store_true', help='Edit an existing user')
        parser.add_argument('--change_password', action='store_true', help='Change password')
        parser.add_argument('--deactivate', action='store_true', help='Deactivate user')

    def handle(self, *args, **options):
        if options['add']:
            email = input('Email: ').strip()

            try:
                validate_email(email)
                user, created = User.objects.get_or_create(email=email)

                if created:
                    user.first_name = input('First Name: ').strip()
                    user.last_name = input('Last Name: ').strip()
                    password = generate_password()
                    user.set_password(password)
                    user.username = user.first_name + ' ' + user.last_name
                    user.save()

                    self.stdout.write(self.style.SUCCESS(f'User created successfully with password: {password}'))
                else:
                    self.stdout.write(self.style.ERROR(f'User "{user.email}" already exists'))
            except ValidationError as e:
                self.stdout.write(self.style.ERROR(f'Invalid email: {e}'))

        elif options['edit']:
            email = input('Enter the email of the user you want to edit: ').strip()
            try:
                user = User.objects.get(email=email)
                self.stdout.write(self.style.SUCCESS(f'Editing user with email: {user.email}'))

                self.stdout.write('User fields:')
                # We iterate through all user fields, but skip those that we won't be modifying
                for field in user._meta.get_fields():
                    if hasattr(user, field.name) and field.name not in IGNORED_USER_FIELDS: 
                        field_value = getattr(user, field.name)

                        while True:
                            answer = input(f'Do you want change {field.verbose_name.upper()}: {field_value}? Confirm (Y/N): ').strip().lower()
                            if answer == 'y':
                                # dodać tutaj zmianę danych
                                new_value = input(f'Enter new value for {field.verbose_name.upper()}: ').strip()
                                setattr(user, field.name, new_value)
                                user.save()
                                self.stdout.write(self.style.SUCCESS(f'Set the new value to: {new_value}'))
                                break

                            elif answer == 'n':
                                break

            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'User with email "{email}" does not exist'))

        elif options['change_password']:
            email = input('Enter the email of the user you want to change password: ').strip()
            try:
                user = User.objects.get(email=email)
                password = generate_password()
                user.set_password(password)
                user.save()
                self.stdout.write(self.style.SUCCESS(f'Password changed to {password}'))

            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'User with email "{email}" does not exist'))

        elif options['deactivate']:
            email = input('Enter the email of the user you want to deactivate: ').strip()
            try:
                user = User.objects.get(email=email)
                user.is_active = False
                user.save()
                self.stdout.write(self.style.SUCCESS(f'User {user.email} has been deactivated'))

            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'User with email "{email}" does not exist'))

        else:
            argument_list = available_arguments(options)
            self.stdout.write(self.style.ERROR(f'Please provide {argument_list} flag'))
