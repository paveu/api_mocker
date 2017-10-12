# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from multiselectfield import MultiSelectField

from .enums import HTTP_METHODS, CONTENT_TYPES, STATUS_CODES


class DefaultModel(models.Model):
    create_date = models.DateTimeField(
        verbose_name='Create date', auto_now_add=True, auto_now=False)
    update_date = models.DateTimeField(
        verbose_name='Update date', auto_now_add=False, auto_now=True)

    class Meta:
        abstract = True


@python_2_unicode_compatible
class ResponseSetting(DefaultModel):
    content_type = models.CharField(
        verbose_name='Content type', max_length=256, choices=CONTENT_TYPES.choices)
    status_code = models.IntegerField(
        verbose_name='HTTP Status code', choices=STATUS_CODES.choices)

    class Meta:
        verbose_name = 'Response setting'
        verbose_name_plural = 'Response settings'

    def __str__(self):
        return ' - '.join([self.content_type, unicode(self.status_code)])


@python_2_unicode_compatible
class Mocker(DefaultModel):
    destination_address = models.URLField(
        max_length=200, verbose_name='API to mock')
    allowed_http_method = MultiSelectField(
        verbose_name='Allowed HTTP method for mock', choices=HTTP_METHODS.choices)
    allowed_content_type = models.CharField(
        verbose_name='Allowed content type for mock', max_length=256, choices=CONTENT_TYPES.choices)
    callback_address = models.URLField(
        max_length=200, verbose_name='Callback address (Optional)', blank=True, null=True)
    callback_content_type = models.CharField(
        verbose_name='Callback content type (Optional)', max_length=256, choices=CONTENT_TYPES.choices,
        blank=True, null=True)
    mocked_address = models.URLField(
        max_length=200, verbose_name='Mocked API', blank=True, null=True)
    hashed_id = models.CharField(
        verbose_name='Hashed ID', max_length=128)
    response_setting = models.ForeignKey(
        ResponseSetting, verbose_name='Response settings (Optional)', null=True, blank=True)

    class Meta:
        verbose_name = 'API Mock'
        verbose_name_plural = 'API Mocks'

    def __str__(self):
        return self.mocked_address


@python_2_unicode_compatible
class CustomHeader(DefaultModel):
    mocker = models.ForeignKey(
        Mocker, verbose_name='Mocker')
    key = models.CharField(
        verbose_name='Key', max_length=256)
    value = models.CharField(
        verbose_name='Value', max_length=256)

    class Meta:
        verbose_name = 'Custom header'
        verbose_name_plural = 'Custom headers'

    def __str__(self):
        return ' - '.join([self.key, unicode(self.value)])


@python_2_unicode_compatible
class ResponseLog(DefaultModel):
    mocker = models.ForeignKey(
        Mocker, verbose_name='Mocker')
    headers = models.TextField(
        verbose_name='Response headers', null=True)
    content = models.TextField(
        verbose_name='Response content', null=True)

    class Meta:
        verbose_name = 'Response Log'
        verbose_name_plural = 'Response logs'

    def __str__(self):
        return self.mocker.destination_address
