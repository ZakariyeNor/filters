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

## 4. Advanced Filtering / Faceted Search

* Move beyond basic filtering and **django-filter**.  
* Implement a **faceted search system** like on Amazon, Zalando, or H&M.  
* Faceted system **filters products** and shows **available options with counts**.

### 4.1 What is Faceted Search?

* **Definition:** Allows users to refine results using multiple filters (category, brand, price, status).  
* **Difference from basic filtering:** Shows **facet counts** for each option, not just applied filters.  
* **Example:**
    * Category:
        * Shoes (123)
        * Shirts (87)
        * Pants (56)
    * Status:
        * Active (200)
        * Inactive (66)
    * Price:
        * Under $50 (140)
        * $50–$100 (90)
        * Over $100 (36)

* Counts **update dynamically** depending on the active filters.

### 4.2 Features to Build

* **Category Facets:**
    * Show a list of categories.  
    * Each category displays the number of products available.  
    * Counts adjust dynamically if other filters (e.g., status, brand) are applied.  

* **Status Facets:**  
    * Example: "Active" vs. "Inactive".  
    * Counts reflect the currently filtered dataset.  

* **Price Buckets:**  
    * Predefined ranges instead of arbitrary numbers.  
    * Example buckets:  
        * Under $50  
        * $50–$100  
        * Over $100  

* **Brand Facets (Optional):**  
    * Display available brands with counts.  
    * Useful for larger product catalogs.  

* **Multi-select Filters:**  
    * Users can select multiple options simultaneously.  
    * Example: Category = Shoes + Shirts, Status = Active

### 4.3 How It Works (Conceptual)

* **Base Query:** Start with the filtered queryset (all products or those matching current filters).  
* **Facet Calculation:** For each filter group (categories, statuses, price ranges), calculate counts of matching products.  
* **Dynamic Updates:** Recalculate facet counts when a user applies filters.  

* **Example flow:**
    1. User loads `/products/` with no filters → show all products and facet counts for every category.  
    2. User selects "Shoes" → product list shows only shoes, facets update to reflect counts within the "Shoes" subset.  
    3. User additionally selects "Active" → only active shoes shown, counts update again.

### 4.4 User Experience (UX) Considerations

* **Checkbox UI:**  
    * Categories, brands, and statuses are best represented as checkboxes (multi-select).  
    * Example: Sidebar with "Shoes [123]" and "Shirts [87]" where both can be selected at once.

* **Price Ranges:**  
    * Predefined ranges make it easier for users than typing custom values.  
    * Use radio buttons (single select) or checkboxes (multi-select).  

* **URL Parameters:**  
    * Each active filter should be reflected in the URL.  
    * Example: `/products/?category=shoes&category=shirts&status=active&price_bucket=under_50`  
    * Ensures filters are **shareable and bookmarkable**.

* **Facet Counts Update:**  
    * Counts must reflect the **current filtered state**, not the full catalog.  
    * Example: Filtering only "Active products" → category counts represent only active products.

### 4.5 Performance Challenges

* **Count Queries:** Calculating counts per category/status can be expensive with thousands of products.  
* **Solutions:**  
    * Use database aggregation efficiently.  
    * Cache facet results for frequently used queries.  
    * Denormalize counts on Category or Brand models and update via signals.

### 4.6 Testing & Validation

* Verify that counts match the **actual number of products** shown.  
* Ensure **multi-select filters** apply correctly.  
* Confirm **URL parameters preserve filters** across pagination.  
* Test combinations of filters (category + brand + price) for correctness.

### 4.7 Acceptance Criteria

* Category facet list displays **dynamic counts**.  
* Status facet list displays **dynamic counts**.  
* Price bucket facet displays **correct ranges**.  
* Multi-select filtering works (selecting multiple categories or brands).  
* Counts update based on **currently applied filters**.  
* Filters persist in the URL (**shareable/bookmarkable**).  
* No unnecessary database queries (verify with **Django Debug Toolbar**).

# Step 5 — Optimizing Filters (Indexes, Relationships, Caching, Monitoring)

**Goal:** Make the product list and faceted queries fast and production-ready. Reduce database queries, avoid N+1 problems, cache expensive computations, and be able to measure query counts in tests.

---

## 5.1 Add Indexes (Schema-Level)

**Purpose:** Improve the speed of queries for frequently filtered fields. Indexes help the database quickly locate and order data.  

**Key Points:**
- Add single-field indexes on frequently filtered fields such as status, price, and created_at.  
- Consider composite indexes for common multi-column queries, for example category + status.  
- Always measure performance impact locally before applying indexes. Indexes speed up reads but slightly slow down writes.  
- Use tools like `EXPLAIN` or Django Debug Toolbar to verify index usage.

---

## 5.2 Avoid N+1 Queries

**Purpose:** Each foreign-key or reverse relationship accessed in a loop can trigger additional database queries, slowing performance.  

**Key Points:**
- Use techniques like eager loading to fetch related objects in the same query.  
- Fetch single-valued relationships (foreign keys or one-to-one) together with the main query.  
- Prefetch multi-valued relationships (many-to-many or reverse foreign keys) efficiently.  
- Ensures templates can access related data without firing extra queries, keeping performance predictable.

---

## 5.3 Cache Filtering Results & Facet Counts

**Purpose:** Computing facets and repeated filter combinations is expensive. Caching reduces redundant database queries and speeds up response times.  

**Key Points:**
- Cache rendered HTML fragments for the product list and active filters.  
- Cache results keyed by filter parameters to ensure correctness.  
- Use a fast cache backend, such as Redis.  
- Invalidate caches on product updates, creations, or deletions to prevent stale data.  
- Coarse cache invalidation is simpler but may temporarily remove more data than necessary; precise invalidation is complex but more efficient.  
- Choose a reasonable cache time-to-live (TTL) to balance freshness and performance.

---

## 5.4 Pagination & Result Limits

**Purpose:** Avoid returning huge result sets that can degrade performance.  

**Key Points:**
- Always paginate product results, e.g., 24 or 48 items per page.  
- When caching, cache the rendered page along with its filters.  
- Avoid fully evaluating large querysets; use slicing to limit the number of records returned.  
- Proper pagination ensures fast rendering and lower memory usage on the server.

---

## 5.5 Monitoring & Diagnostics

**Purpose:** Measure query performance, detect inefficiencies, and prevent regressions.  

**Key Points:**
- Use tools like Django Debug Toolbar for development.  
- Production monitoring can use Datadog, New Relic, or similar tools.  
- Capture the number of queries executed per view or template rendering to detect N+1 issues.  
- Set a query budget (maximum allowed queries) for each page and enforce it via automated tests.  
- Review captured queries to ensure that related object accesses in templates do not add extra queries.

---

## 5.6 Denormalization: Product Count on Category

**Purpose:** Avoid computing COUNT() queries for categories on every request.  

**Key Points:**
- Maintain a `product_count` field on each category that is updated automatically.  
- Increment the count when a new product is added to the category.  
- Decrement the count when a product is deleted.  
- Use signals or hooks to ensure counts are always consistent.  
- Consider bulk operations or management commands for initial backfill or re-calculation.

---

## 5.7 Test Query Count for Denormalized Facets

**Purpose:** Ensure denormalization and caching work as intended without introducing hidden queries.  

**Key Points:**
- Capture queries during template rendering to confirm no extra database hits occur.  
- Test that removing or updating products updates the cached counts correctly.  
- Validate that multi-select facets do not trigger unexpected additional queries.  

---

## 5.8 Summary / Acceptance Criteria

**Expected Outcomes:**
- Product list pages perform within an acceptable query budget (e.g., ≤ 6 queries).  
- Facet counts are precomputed or cached, minimizing repeated COUNT() queries.  
- No N+1 queries exist in templates.  
- Pagination, caching, and denormalized counts combine to ensure fast, predictable filtering performance.  
- Indexes are used efficiently to speed up queries on large datasets.  
- Monitoring and automated tests enforce performance standards.

---

**Notes:**  
- Always balance read optimization with write performance.  
- Regularly review query plans and caching strategies as data grows.  
- Document and track all optimizations to maintain maintainable and scalable code.
