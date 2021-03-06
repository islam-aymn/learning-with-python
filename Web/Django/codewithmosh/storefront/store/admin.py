from django.contrib import admin
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode

from . import models


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["title", "unit_price", "inventory_status", "collection_title"]
    list_editable = ["unit_price"]
    list_per_page = 10
    list_select_related = ["collection"]

    def collection_title(self, product: models.Product):
        return product.collection.title

    @admin.display(ordering="inventory")
    def inventory_status(self, product):
        if product.inventory < 10:
            return "Low"
        return "OK"


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "membership", "orders_count"]
    list_editable = ["membership"]
    list_per_page = 10
    search_fields = ["first_name__istartswith", "last_name__istartswith"]

    @admin.display(ordering="orders_count")
    def orders_count(self, customer: models.Customer):
        url = (
            reverse("admin:store_order_changelist")
            + "?"
            + urlencode({"customer_id": str(customer.pk)})
        )
        return format_html("<a href='{}'>{}</a>", url, customer.orders_count)

    def get_queryset(self, request):
        return (
            super(CustomerAdmin, self)
            .get_queryset(request)
            .annotate(orders_count=Count("order"))
        )


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "placed_at", "customer", "payment_status"]


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ["title", "products_count"]

    @admin.display(ordering="products_count")
    def products_count(self, collection):
        url = (
            reverse("admin:store_product_changelist")
            + "?"
            + urlencode({"collection_id": str(collection.pk)})
        )
        return format_html("<a href='{}'>{}</a>", url, collection.products_count)

    def get_queryset(self, request):
        return (
            super(CollectionAdmin, self)
            .get_queryset(request)
            .annotate(products_count=Count("product"))
        )


admin.site.register(
    (
        models.Address,
        models.Cart,
        models.CartItem,
        models.Promotion,
    )
)
