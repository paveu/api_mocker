from django.contrib import admin
from .models import Mocker


class MockerAdmin(admin.ModelAdmin):
    date_hierarchy = 'creation_date'
    ordering = ('-creation_date',)
    exclude = ('hashed_id',)

    list_display = (
        'mocked_address',
        'allowed_http_method',
        'original_destination_address',
        'allowed_destination_content_type',
        'callback_address',
        'callback_content_type',
        )

admin.site.register(Mocker, MockerAdmin)
