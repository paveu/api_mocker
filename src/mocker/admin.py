from django.contrib import admin
from .models import Mocker


class MockerAdmin(admin.ModelAdmin):
    date_hierarchy = 'creation_date'
    ordering = ('-creation_date',)
    exclude = ('short_id',)

    list_display = (
        'mocked_address',
        'http_method',
        'destination_address',
        'destination_content_type',
        'return_address', 
        'return_content_type', 
        )

admin.site.register(Mocker, MockerAdmin)
