from django.core.management.base import BaseCommand
from accounts.models import Ph, Rks
from accounts.management.commands._private import search_user, search_shop, available_arguments


class Command(BaseCommand):
    help = 'Add and remove Rks role'

    def add_arguments(self, parser):
        parser.add_argument('--add', action='store_true', help='Add an Rks role ',)
        parser.add_argument('--remove', action='store_true', help='Remove an Rks role')
        parser.add_argument('--assign-shops', action='store_true', help='Assign the shops to the Rks')

    def handle(self, *args, **options):
        if options['add']:
            user = search_user(self)
            if user:
                if not Ph.objects.filter(user=user).exists():
                    rks, created = Rks.objects.get_or_create(user=user)
                    if created:
                        self.stdout.write(self.style.SUCCESS(f'{rks.user.email} is now a Rks'))
                    else:
                        self.stdout.write(self.style.ERROR(f'{user.email} is already a Rks'))
                else:
                    self.stdout.write(self.style.ERROR(f'{user.email} is Ph and can not be Rks'))


        elif options['remove']:
            user = search_user(self)
            if user:
                if Rks.objects.filter(user=user).exists():
                    user.rks.delete()
                    self.stdout.write(self.style.SUCCESS(f'Rks role was successfully removed from {user.email}'))
                else:
                    self.stdout.write(self.style.ERROR(f'{user.email} is not Rks'))

        elif options['assign_shops']:
            user = search_user(self)
            if user:
                if Rks.objects.filter(user=user).exists():
                    while True:
                        shop = search_shop(self)
                        if shop:
                            if shop.rks:
                                answer = input(f'{shop.shop_id} has Rks: {shop.rks.user.email} Do you want change it? Confirm(Y/N)').strip().lower()
                                if answer == 'y':
                                    shop.rks = user.rks
                                    shop.save()
                                    self.stdout.write(self.style.SUCCESS(f'{user.email} successfully assigned to {shop.shop_id}'))
                                elif answer == 'n':
                                    self.stdout.write(self.style.ERROR(f'{shop.rks.user.email} is still Rks of {shop.shop_id}'))

                            else:
                                answer = input(f'Do you want to assign {shop.shop_id} to {user.email}? Confirm(Y/N)').strip().lower()
                                if answer == 'y':
                                    shop.rks = user.rks
                                    shop.save()
                                    self.stdout.write(self.style.SUCCESS(f'{user.email} successfully assigned to {shop.shop_id}'))

                                elif answer == 'n':
                                    self.stdout.write(self.style.ERROR(f'{user.email} has not been assigned to {shop.shop.id}'))
                                    continue
                        else:
                            break
                else:
                    self.stdout.write(self.style.ERROR(f'{user.email} is not Rks'))



        else:
            argument_list = available_arguments(options)
            self.stdout.write(
                    self.style.ERROR(f'Please provide {argument_list} flag')
                )
