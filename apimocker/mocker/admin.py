from django.contrib import admin

from .models import Mocker, ResponseSetting, ResponseLog


class MockerAdmin(admin.ModelAdmin):
    date_hierarchy = 'create_date'
    ordering = ('-create_date',)
    exclude = ('hashed_id',)

    list_display = (
        'destination_address',
        'allowed_http_method',
        'allowed_content_type',
        'callback_address',
        'callback_content_type',
        'mocked_address',
    )


class ResponseSettingAdmin(admin.ModelAdmin):
    date_hierarchy = 'create_date'
    ordering = ('-create_date',)


class ResponseLogAdmin(admin.ModelAdmin):
    date_hierarchy = 'create_date'
    ordering = ('-create_date',)


admin.site.register(Mocker, MockerAdmin)
admin.site.register(ResponseSetting, ResponseSettingAdmin)
admin.site.register(ResponseLog, ResponseLogAdmin)
