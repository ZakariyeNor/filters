from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    product_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    STATUS_CHOICES = (("active","Active"),("inactive","Inactive"))

    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, related_name="products")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, db_index=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, db_index=True)
    stock = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=["category", "status"]),
            models.Index(fields=["-created_at"]),
        ]

    def __str__(self):
        return self.name
