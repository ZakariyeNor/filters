# Step 0 — Project Setup & Sample Data

**Goal:**  
Set up the Django project with a `products` app and generate realistic sample data for testing filters.

---

## 1. Setup

- Create a project folder named `filters_project`, navigate into it, create a Python virtual environment called `env`, and activate it.  
- Install dependencies: Django, Django REST Framework, django-filter, factory_boy, Faker, and django-debug-toolbar using pip.  
- Start a new Django project named `filters_project` and a new app named `products`.  
- Add the app and required packages to `INSTALLED_APPS` in `settings.py`.

---

## 2. Models

- **Category** — name field.  
- **Brand** — name field.  
- **Product** — name, category, brand, status, price, stock, and created_at fields.  
- Indexes are added on frequently filtered fields for efficiency.

---

## 3. Admin

- Register models with list display and filters for easy inspection.  
- Access the admin at `http://127.0.0.1:8000/admin/`.

---

## 4. Factories & Sample Data

- Use **factory_boy** and **Faker** to generate products.  
- Products are randomly assigned to **10 fixed categories** and **30 fixed skincare brands**.  
- Generate 1000 products using the management command `generate_products`.

---

## 5. Categories (10)

Cleansers, Toners & Mists, Moisturizers, Serums & Oils, Exfoliators, Masks, Eye Care, Lip Care, Sun Care, Treatment & Specialty

---

## 6. Brands (30+)

The Ordinary, La Roche-Posay, CeraVe, Neutrogena, Bioderma, Kiehl’s, Clinique, L’Oréal Paris, Olay, Nivea, Aveeno, Eucerin, Vichy, Dr. Jart+, Garnier, Paula’s Choice, Skinceuticals, Shiseido, Laneige, Innisfree, Cosrx, Sulwhasoo, Drunk Elephant, Origins, Murad, Peter Thomas Roth, Herbivore, First Aid Beauty, Youth to the People, Elemis

---

## 7. Verification

Check that the products were created successfully and the database is populated with:

- Django project runs without errors.  
- Admin shows all models.  
- 1000 products distributed across the 10 categories and 30 brands, ready for filtering and testing.


# Step 1 — Basic Filtering with QuerySets

**Goal:**  
Become fluent at writing Django ORM filters in the shell to retrieve targeted subsets of products.

---

## 1. Import Models

Open the Django shell:

```bash
python manage.py shell

from products.models import Product, Category, Brand
from django.db.models import Q

Basic Filters

Filter by category and status:
Product.objects.filter(category__name="Cleansers", status="active")

Filter by brand:
Product.objects.filter(brand__name="The Ordinary", status="active")

Lookup Types

Case-insensitive contains:
Product.objects.filter(name__icontains="vitamin")


Price range:
Product.objects.filter(price__gte=50, price__lte=200)


Filter by date:
Product.objects.filter(created_at__date="2025-10-01")

Chaining & Excluding

# Active products in stock
Product.objects.filter(status="active").exclude(stock__lte=0)

# Filter by category and price range
Product.objects.filter(category__name="Moisturizers", price__lte=100).exclude(stock=0)

Q Objects (Complex / OR Queries)
from django.db.models import Q

# Products in Cleansers OR brand containing "Neutrogena"
Product.objects.filter(Q(category__name="Cleansers") | Q(brand__name__icontains="Neutrogena"))

# Active products either under 50 or stock less than 10
Product.objects.filter(Q(price__lt=50) | Q(stock__lt=10), status="active")


Combine using & (AND), | (OR), and negate with ~ (NOT).

Ordering

# Highest priced active products first
Product.objects.filter(status="active").order_by("-price")

# Oldest products first
Product.objects.order_by("created_at")
```

## 7. Exercises

1. List all products in **"Masks"** category with stock > 0.  
2. List products from **"La Roche-Posay"** with price between 50 and 200.  
3. Find all products containing **"cream"** in the name.  
4. Get **active products** ordered by price descending.  
5. List products created in the **last 30 days**.  
6. List products in categories **"Serums & Oils"** or **"Moisturizers"**.  
7. List products **not in stock** (`stock=0`).  
8. List **active products** with brand containing **"Neutrogena"** OR **"CeraVe"**.  
9. List products priced **below 100** but with **stock greater than 50**.  
10. List products **excluding categories** "Treatment & Specialty" and "Sun Care".  
