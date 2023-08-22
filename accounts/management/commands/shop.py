from django.core.management.base import BaseCommand
from accounts.models import Shop
from accounts.management.commands._private import DISTRICT, REGION, validate_shop_id, available_arguments


class Command(BaseCommand):
    help = 'Create and edit shop'
    
    def add_arguments(self, parser):
        parser.add_argument('--add', action='store_true', help='Add new shop')
        parser.add_argument('--edit', action='store_true', help='Edit shop')

    def handle(self, *args, **options):
        if options['add']:
            shop_id = input('Enter shop ID: ').strip() 
            if validate_shop_id(shop_id):

                shop, created = Shop.objects.get_or_create(shop_id=shop_id.upper())

                if created:
                    print('Choose District')
                    for i in enumerate(DISTRICT):
                        print(i)
                    while True:
                        try:
                            district = int(input('Choose number corresponding to the District: '))
                            shop.district = DISTRICT[district]
                            self.stdout.write(
                                    self.style.SUCCESS(f'District set to: {DISTRICT[district]}.')
                                )
                            break
                        except Exception as e:
                            self.stdout.write(
                                    self.style.ERROR(f'Invalid input. Please enter a valid number. {e}')
                                )

                    print('Choose Region')
                    for i in enumerate(REGION):
                        print(i)
                    while True:
                        try:
                            region = int(input('Choose number corresponding to the Region: '))
                            shop.region = REGION[region]
                            self.stdout.write(
                                    self.style.SUCCESS(f'Region set to: {REGION[region]}.')
                                )
                            shop.save()
                            self.stdout.write(
                                    self.style.SUCCESS(f'Shop {shop.shop_id} created successfully. District set to: {shop.district}. Region set to: {shop.region}.')
                                )
                            break
                        except Exception as e:
                            self.stdout.write(
                                    self.style.ERROR(f'Invalid input. Please enter a valid number. {e}')
                                )

                else:
                    self.stdout.write(
                            self.style.ERROR(f'Shop with ID {shop.shop_id} already exists.')
                        )

            else:
                self.stdout.write(
                        self.style.ERROR('Shop ID must be 5 characters long and have the first two as characters and the last three as digits, e.g. "FA001".')
                    )

        elif options['edit']:
            shop_id = input('Enter shop ID which you want to edit: ').strip().upper()
            try:
                shop = Shop.objects.get(shop_id=shop_id)
                self.stdout.write(self.style.SUCCESS(f'Editing shop with ID: {shop.shop_id}.'))

                while True:
                    answer = input(f'Do you want change District: {shop.district}? Confirm (Y/N): ').strip().lower()
                    if answer == 'y':
                        print('Choose District')
                        for i in enumerate(DISTRICT):
                            print(i)
                        while True:
                            try:
                                district = int(input('Choose number corresponding to the District: '))
                                shop.district = DISTRICT[district]
                                self.stdout.write(
                                        self.style.SUCCESS(f'District changed to {DISTRICT[district]}.')
                                    )
                                break
                            except Exception as e:
                                self.stdout.write(
                                        self.style.ERROR(f'Invalid input. Please enter a valid number. {e}')
                                    )
                        break

                    elif answer == 'n':
                        break

                while True:
                    answer = input(f'Do you want change Region: {shop.region}? Confirm (Y/N): ').strip().lower()
                    if answer == 'y':
                        print('Choose Region')
                        for i in enumerate(REGION):
                            print(i)
                        while True:
                            try:
                                region = int(input('Choose number corresponding to the Region: '))
                                shop.region = REGION[region]
                                self.stdout.write(
                                        self.style.SUCCESS(f'Region changed to {REGION[region]}')
                                    )
                                break
                            except Exception as e:
                                self.stdout.write(
                                        self.style.ERROR(f'Invalid input. Please enter a valid number. {e}')
                                    )

                        break

                    elif answer == 'n':
                        break

                shop.save()

                self.stdout.write(
                        self.style.SUCCESS(f'Shop {shop.shop_id} updated successfully. District: {shop.district}. Region: {shop.region}.')
                    )

            except Shop.DoesNotExist:
                self.stdout.write(
                        self.style.ERROR(f'Shop with ID "{shop_id}" does not exist')
                    )                   

        else:
            argument_list = available_arguments(options)
            self.stdout.write(
                    self.style.ERROR(f'Please provide {argument_list} flag')
                )
