from django.contrib import admin

from .models import Order


@admin.register(Order)
class WorkPriceAdmin(admin.ModelAdmin):
    search_fields = ['master', 'type_work']
    list_display = ['master', 'type_work', 'date_of_completion']
