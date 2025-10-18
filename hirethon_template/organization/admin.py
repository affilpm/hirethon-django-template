from django.contrib import admin
from .models import Organization, Membership, Namespace, ShortURL, BulkUpload

admin.site.register(Organization)
admin.site.register(Membership)
admin.site.register(Namespace)
admin.site.register(ShortURL)
admin.site.register(BulkUpload)