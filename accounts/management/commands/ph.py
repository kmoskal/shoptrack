from django.core.management.base import BaseCommand
from django.db import IntegrityError
from accounts.models import Ph
from accounts.management.commands._private import search_user, search_shop, create_validate_employee_id, available_arguments


class Command(BaseCommand):
    help = 'Add and remove a sales rep to the employee'

    def add_arguments(self, parser):
        parser.add_argument('--add', action='store_true', help='Add a sales rep to the employee')
        parser.add_argument('--edit', action='store_true', help='Edit sales rep')
        parser.add_argument('--remove', action='store_true', help='Remove a sales rep from the employee')

    def handle(self, *args, **options):
        if options['add']:
            user_to_assign = search_user(self)
            if not Ph.objects.filter(user=user_to_assign).exists():
                if user_to_assign:
                    shop_to_assign = search_shop(self)

                    if user_to_assign and shop_to_assign:
                        try:
                            employee_id = create_validate_employee_id((shop_to_assign))
                            employee_ifs = int(input('Enter employee IFS: '))
                            ph: PH = Ph.objects.create(
                                user=user_to_assign,
                                shop=shop_to_assign,
                                employee_id=employee_id,
                                employee_ifs=employee_ifs
                            )
                            ph.save()
                            self.stdout.write(self.style.SUCCESS(f'{ph.user.username} was added to {ph.shop.shop_id}'))
                        except ValueError as e:
                            self.stdout.write(self.style.ERROR(f'ValueError {e}'))
                        except IntegrityError as e:
                            self.stdout.write(self.style.ERROR(f'IntegrityError {e}'))
                        except Exception as e:
                            self.stdout.write(self.style.ERROR(f'Exception {e}'))
            else:
                self.stdout.write(self.style.ERROR(f'{user_to_assign.username} is already a PH'))

        elif options['edit']:
            user_to_edit = search_user(self)
            if user_to_edit:
                try:
                    ph = Ph.objects.get(user_id=user_to_edit.id)
                    new_shop = search_shop(self)
                    if new_shop:
                        new_employee_id = create_validate_employee_id(new_shop)
                        if new_employee_id:
                            ph.shop = new_shop
                            ph.employee_id = new_employee_id
                            ph.save()
                            self.stdout.write(self.style.SUCCESS(f'{ph.user.username} was added to {ph.shop.shop_id}'))
                        else:
                            self.stdout.write(self.style.ERROR(f'Employee_id must be valid. You pass {new_employee_id}'))
                    else:
                        self.stdout.write(self.style.ERROR(f'You must enter valid Shop ID'))

                except Ph.DoesNotExist as e:
                    self.stdout.write(self.style.ERROR(f'{user_to_edit.username} is not a PH'))
                except IntegrityError as e:
                    self.stdout.write(self.style.ERROR(f'{e}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'{e}'))

        elif options['remove']:
            user = search_user(self)
            if user:
                try:
                    ph = Ph.objects.get(user_id=user.id)
                    ph.delete()
                    self.stdout.write(self.style.SUCCESS(f'{user.username} was remove from PH role'))
                except Ph.DoesNotExist as e:
                    self.stdout.write(self.style.ERROR(f'{user.username} is not a PH'))

        else:
            argument_list = available_arguments(options)
            self.stdout.write(self.style.ERROR(f'Please provide {argument_list} flag'))
