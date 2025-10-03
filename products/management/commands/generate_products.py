from django.core.management.base import BaseCommand
from products.factories import ProductFactory, CategoryFactory, BrandFactory
from products.models import Category, Brand

class Command(BaseCommand):
    help = "Generate 1000 sample skincare products using fixed categories and brands"

    def add_arguments(self, parser):
        parser.add_argument("--count", type=int, default=1000, help="Number of products to create")

    def handle(self, *args, **kwargs):
        count = kwargs["count"]

        # Create fixed categories if they don't exist
        CATEGORY_NAMES = [
            "Cleansers", "Toners & Mists", "Moisturizers", "Serums & Oils",
            "Exfoliators", "Masks", "Eye Care", "Lip Care", "Sun Care", "Treatment & Specialty"
        ]
        for name in CATEGORY_NAMES:
            Category.objects.get_or_create(name=name)

        # Create fixed brands if they don't exist
        BRAND_NAMES = [
            "The Ordinary", "La Roche-Posay", "CeraVe", "Neutrogena", "Bioderma",
            "Kiehl’s", "Clinique", "L’Oréal Paris", "Olay", "Nivea",
            "Aveeno", "Eucerin", "Vichy", "Dr. Jart+", "Garnier",
            "Paula’s Choice", "Skinceuticals", "Shiseido", "Laneige", "Innisfree",
            "Cosrx", "Sulwhasoo", "Drunk Elephant", "Origins", "Murad",
            "Peter Thomas Roth", "Herbivore", "First Aid Beauty", "Youth to the People", "Elemis"
        ]
        for name in BRAND_NAMES:
            Brand.objects.get_or_create(name=name)

        # Generate products
        for _ in range(count):
            ProductFactory()

        self.stdout.write(self.style.SUCCESS(f"{count} products created successfully!"))
