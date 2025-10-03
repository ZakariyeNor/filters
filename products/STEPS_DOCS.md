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


# Step 2 – Filtering Products in Views Using GET Parameters

## Overview

In Step 2, we focus on **adding basic filtering functionality** to your Django project.  
This allows users to **narrow down the list of products** based on different criteria, such as category, price range, or status (active/inactive).  

Instead of using any external packages yet, we handle this **directly in the Django view** using **GET parameters** from the URL.

---

## How Filtering Works

1. **Capture Query Parameters**  
   - When a user selects filters in the interface (e.g., category dropdown, price fields), their choices are sent to the server as **query parameters**.  
   - These parameters appear in the URL, for example:  
     ```
     /products/?category=Cleansers&min_price=10&status=active
     ```

2. **Apply Filters in the View**  
   - In the Django view, we read the query parameters from `request.GET`.  
   - For each filter (category, min/max price, status), we **check if the user provided a value**.  
   - Only if a value exists, we **narrow down the list of products** accordingly.

3. **Price Filtering**  
   - Users can set a minimum and/or maximum price.  
   - The view ensures products are only included if their price is within the specified range.

4. **Status Filtering**  
   - Products may have different statuses (like "active" or "inactive").  
   - This filter allows users to see only products that are currently active, for instance.

5. **Pagination**  
   - When filtering returns many results, we split the products into pages.  
   - Pagination keeps the current filters applied, so users can navigate through pages without losing their selected criteria.

---

## What the User Sees

- A **filter form** at the top of the product list allows selecting category, entering price range, and choosing status.  
- After clicking “Apply,” the page reloads, showing only products that match the selected filters.  
- Pagination links maintain all selected filters, making browsing smooth.

---

## Key Takeaways

- Using GET parameters is a simple way to **filter querysets without extra packages**.  
- Always **check if a parameter exists** before applying a filter to avoid errors.  
- This step sets the foundation for more advanced filtering using tools like **Django Filter**, which will be introduced in Step 3.


# Step 3 — django-filter Integration (FilterSet + Clean URLs)

## Goal
In this step we move from manual GET parameter parsing to using the django-filter package.  
This reduces boilerplate code and gives us more powerful filters such as ranges, multiple choice fields, and date filters.  
It also makes our filtering logic cleaner, reusable, and keeps the URLs human-readable.

---

## Installation and Setup
First, install the django-filter package and add it to INSTALLED_APPS in settings.py.  
This ensures Django knows about the filter framework and can render filter forms automatically.

---

## Defining a FilterSet
A FilterSet is like a form class for filters.  
We define which fields we want to filter on (such as category, brand, price range, and status).  
Each filter can have its own widget styling, like a select dropdown for categories and brands, or number inputs for min and max price.  
This step replaces writing if-statements manually in the view.

---

## Creating a Filter View
Instead of writing filtering logic by hand in the view, we use django-filter’s FilterView.  
This integrates directly with our Product model, applies the FilterSet automatically, and gives us pagination and context data without boilerplate.  
It also ensures the filter form is available in the template via filter.form.

---

## Updating URLs
The URL mapping points the root path to the ProductFilterView.  
Now, when visiting the product list page, the filter form will render automatically, and GET query parameters will be used to filter results.  
For example: /?category=1&brand=2&min_price=50&max_price=200.

---

## Template Usage
In the template, we render the filter form fields directly.  
Each filter field (category, brand, min price, max price, status) will show up as a styled input or select box.  
We also add an “Apply” button to submit the filters.  
Below the form, we render the product grid and handle empty states (e.g., no products found).

---

## Acceptance Criteria
- URL query parameters automatically connect to filters (no manual parsing).  
- Range filters like minimum price and maximum price work correctly.  
- Choice filters like status and dropdowns for category and brand are functional.  
- Pagination still works together with the filters.  
- The filter form is styled and user-friendly.

---

## Example URLs
- Filtering by category and brand: `/?category=1&brand=2`  
- Filtering by price range: `/?min_price=50&max_price=200`  
- Filtering by category and status: `/?category=3&status=inactive`

---
