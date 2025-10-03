import random
from faker import Faker
from factory.django import DjangoModelFactory
from factory import LazyAttribute
from products.models import Product, Category, Brand

fake = Faker()

# Fixed lists
CATEGORY_NAMES = [
    "Cleansers",
    "Toners & Mists",
    "Moisturizers",
    "Serums & Oils",
    "Exfoliators",
    "Masks",
    "Eye Care",
    "Lip Care",
    "Sun Care",
    "Treatment & Specialty"
]

BRAND_NAMES = [
    "The Ordinary", "La Roche-Posay", "CeraVe", "Neutrogena", "Bioderma",
    "Kiehl’s", "Clinique", "L’Oréal Paris", "Olay", "Nivea",
    "Aveeno", "Eucerin", "Vichy", "Dr. Jart+", "Garnier",
    "Paula’s Choice", "Skinceuticals", "Shiseido", "Laneige", "Innisfree",
    "Cosrx", "Sulwhasoo", "Drunk Elephant", "Origins", "Murad",
    "Peter Thomas Roth", "Herbivore", "First Aid Beauty", "Youth to the People", "Elemis"
]

# Factories
class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    name = LazyAttribute(lambda _: random.choice(CATEGORY_NAMES))


class BrandFactory(DjangoModelFactory):
    class Meta:
        model = Brand

    name = LazyAttribute(lambda _: random.choice(BRAND_NAMES))


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    name = LazyAttribute(lambda _: fake.sentence(nb_words=3))
    category = LazyAttribute(lambda _: random.choice(Category.objects.all()))
    brand = LazyAttribute(lambda _: random.choice(Brand.objects.all()))
    status = LazyAttribute(lambda _: fake.random_element(["active", "inactive"]))
    price = LazyAttribute(lambda _: round(fake.pydecimal(left_digits=3, right_digits=2, positive=True), 2))
    stock = LazyAttribute(lambda _: fake.random_int(min=0, max=200))
    created_at = LazyAttribute(lambda _: fake.date_time_between(start_date="-18M", end_date="now"))
