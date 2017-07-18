# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models

from .enums import HTTP_METHODS, CONTENT_TYPES, STATUS_CODES


class DefaultModel(models.Model):
    create_date = models.DateTimeField(verbose_name='Create date', auto_now_add=True, auto_now=False)
    update_date = models.DateTimeField(verbose_name='Update date', auto_now_add=False, auto_now=True)

    class Meta:
        abstract = True


class ResponseSetting(DefaultModel):
    content_type = models.CharField(verbose_name='Content type', max_length=256, choices=CONTENT_TYPES.choices)
    status_code = models.IntegerField(verbose_name='HTTP Status code', choices=STATUS_CODES.choices)

    class Meta:
        verbose_name = 'Response setting'
        verbose_name_plural = 'Response settings'

    def __unicode__(self):
        return ' - '.join([self.content_type, unicode(self.status_code)])


class Mocker(DefaultModel):
    destination_address = models.URLField(max_length=200, verbose_name='API to mock')
    allowed_http_method = models.CharField(verbose_name='Allowed HTTP method for mock', max_length=256,
                                           choices=HTTP_METHODS.choices)
    allowed_content_type = models.CharField(verbose_name='Allowed content type for mock', max_length=256,
                                            choices=CONTENT_TYPES.choices)
    callback_address = models.URLField(max_length=200, verbose_name='Callback address', blank=True, null=True)
    callback_content_type = models.CharField(verbose_name='Callback content type', max_length=256,
                                             choices=CONTENT_TYPES.choices, blank=True, null=True)
    mocked_address = models.URLField(max_length=200, verbose_name='Mocked API', blank=True, null=True)
    hashed_id = models.CharField(verbose_name='Hashed ID', max_length=128)
    response_data = models.ForeignKey(ResponseSetting, null=True)

    class Meta:
        verbose_name = 'API Mock'
        verbose_name_plural = 'API Mocks'

    def __unicode__(self):
        return unicode(self.mocked_address)


class ResponseLog(DefaultModel):
    headers = models.TextField(verbose_name='Response headers', null=True)
    content = models.TextField(verbose_name='Response content', null=True)
    mocker = models.ForeignKey(Mocker, null=True)

    class Meta:
        verbose_name = 'Response Log'
        verbose_name_plural = 'Response logs'

    def __unicode__(self):
        return unicode(self.mocker.destination_address)
