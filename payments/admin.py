from django.contrib import admin
from .models import Payment

admin.site.site_header='The dotSchool Admin Portal'
admin.site.index_title='Payments Dashboard'

admin.site.register(Payment)


