from django.contrib import admin
from .models import Category, Product, Commande

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_added')
    search_fields = ('name',)
    ordering = ('-date_added',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'category', 'date_added')
    list_filter = ('category', 'date_added')
    search_fields = ('title', 'description')
    ordering = ('-date_added',)

@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = ('items', 'nom', 'email', 'address', 'ville', 'pays', 'zipcode', 'date_commande')
    list_filter = ('ville', 'pays', 'date_commande')
    search_fields = ('nom', 'email', 'ville', 'pays')
    date_hierarchy = 'date_commande'
    ordering = ('-date_commande',)
