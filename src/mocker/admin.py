from django.contrib import admin
from .models import Mocker


class MockerAdmin(admin.ModelAdmin):
    date_hierarchy = 'creation_date'
    ordering = ('-creation_date',)
    list_display = ('destination_address', 'destination_content_type', 'return_address', 'return_content_type', 'short_id')

admin.site.register(Mocker, MockerAdmin)
