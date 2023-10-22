from django.core.management.base import BaseCommand
from accounts.models import User, Ph, Kss
from accounts.management.commands._private import search_user, available_arguments


class Command(BaseCommand):
    help = 'Add and remove Kss role to Ph'

    def add_arguments(self, parser):
        parser.add_argument('--add', action='store_true', help='Add a Kss role to the Ph',)
        parser.add_argument('--remove', action='store_true', help='Remove a Kss role from the Ph')

    def handle(self, *args, **options):
        if options['add']:
            try:
                user= search_user(self)
                if user:
                    if Ph.objects.filter(user=user).exists():
                        # Check if someone is already kss in user's shop
                        shop_employees = User.objects.filter(ph__shop__shop_id=user.ph.shop.shop_id)
                        kss = [employee.email  for employee in shop_employees if Kss.objects.filter(ph__user=employee).exists()]
                        if kss:
                            self.stdout.write(self.style.ERROR(f'This shop already has a kss {kss}'))
                        else:
                            kss = Kss.objects.create(ph=user.ph)
                            self.stdout.write(self.style.SUCCESS(f'{kss.ph.user.email} is Kss now.'))
                    else:
                        self.stdout.write(self.style.ERROR(f'{user.email} is not Ph'))
            except Exception as e:
                print(f'{e}')

        elif options['remove']:
            try:
                user= search_user(self)
                if Kss.objects.filter(ph__user=user).exists():
                   user.ph.kss.delete()
                   self.stdout.write(self.style.SUCCESS(f'User was deleted successfully'))
                else:
                   self.stdout.write(self.style.ERROR(f'{user.email} is not Kss.'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'{e}'))

        else:
            argument_list = available_arguments(options)
            self.stdout.write(self.style.ERROR(f'Please provide {argument_list} flag'))
