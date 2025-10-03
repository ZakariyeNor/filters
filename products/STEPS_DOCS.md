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
