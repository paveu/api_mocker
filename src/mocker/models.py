from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
 


class DefaultModel(models.Model):
    creation_date = models.DateTimeField(verbose_name='Creation date',
                                         auto_now_add=True,
                                         auto_now=False)
    updation_date = models.DateTimeField(verbose_name='Updation date',
                                         auto_now_add=False,
                                         auto_now=True)

    class Meta:
        abstract = True

class Mocker(DefaultModel):
    HTTP_METHOD_CHOICES = (
        ('POST', 'POST'),
        ('GET', 'GET'),
        # ('PATCH', 'PATCH'),
        # ('DELETE', 'DELETE')
        )
    CONTENT_TYPE_CHOICES = (
        ('application/json', 'application/json'),
        # ('application/x-www-form-urlencoded', 'application/x-www-form-urlencoded'),
        # ('application/xhtml+xml', 'application/xhtml+xml'),
        # ('multipart/form-data', 'multipart/form-data'),
        # ('text/css', 'text/css'),
        # ('text/csv', 'text/csv'),
        # ('text/html', 'text/html'),
        # ('text/json', 'text/json'),
        # ('text/plain', 'text/plain'),
        # ('text/xml', 'text/xml'),
    )
    
    destination_address = models.URLField(
        max_length=200,
        verbose_name='Destination API address to be mocked')
    # http_method = models.ManyToManyField(HTTP_Method, verbose_name='Allowed HTTP methods for mocked address')
    http_method = models.CharField(
        verbose_name='Allowed HTTP method for a mocked API',
        max_length=256,
        choices=HTTP_METHOD_CHOICES)
    destination_content_type = models.CharField(
        verbose_name='Allowed content type for a mocked API',
        max_length=256,
        choices=CONTENT_TYPE_CHOICES)
    return_address = models.URLField(
        max_length=200,
        verbose_name='Callback API address',
        blank=True,
        null=True)
    return_content_type = models.CharField(
        verbose_name='Callback API content type',
        max_length=256,
        choices=CONTENT_TYPE_CHOICES)
    short_id = models.CharField(
        verbose_name='Hashed ID',
        max_length=128)
    mocked_address = models.URLField(
        max_length=200,
        verbose_name='Mocked API Address',
        blank=True,
        null=True)
        
    class Meta:
        verbose_name = 'Mocked API'
        verbose_name_plural = 'Mocked APIs'

    def __unicode__(self):
        return str(self.id)
