from django.contrib import admin
from cars.models import Brand, Car, CarInventory
# Register your models here.

class CarAdmin(admin.ModelAdmin):
    list_display = ('model', 'brand', 'factory_year', 'model_year', 'value',)
    search_fields = ('model', 'brand', 'factory_year', 'model_year', 'value',)

class CarInventoryAdmin(admin.ModelAdmin):
    list_display = ('cars_count', 'cars_value', 'created_at',)
    search_fields = ('cars_count', 'cars_value', 'created_at',)

class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


admin.site.register(Brand, BrandAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(CarInventory, CarInventoryAdmin)



