
from django.core.management.base import BaseCommand
from base.models import Product, Category, User

class Command(BaseCommand):
    help = 'Populate the database with static data'

    def handle(self, *args, **kwargs):
        # Create categories
        categories = [
            {'name': 'Category 1'},
            {'name': 'Category 2'},
            {'name': 'Category 3'},
            {'name': 'Category 4'}
        ]
        for category_data in categories:
            Category.objects.get_or_create(**category_data)

        # Create products
        products = [
            {
                'name': 'Product 1',
                'category': Category.objects.get(name='Category 1'),
                'price': 19.99,
                'description': 'Description of Product 1',
                'availability': True,
                'rate': 4.5,
                'product_quantity': 100,
                'owner': User.objects.first(),  # You may need to adjust this based on your user data
            },
            # Add more products here
        ]
        for product_data in products:
            Product.objects.get_or_create(**product_data)

        self.stdout.write(self.style.SUCCESS('Static data populated successfully'))
