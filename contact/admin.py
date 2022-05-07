'''admin.py'''
from django.contrib import admin
from .models import Contact

# Register your models here.
class ContactAdmin(admin.ModelAdmin):
    '''This Configures the admin site for Contact Model'''
    fieldsets = [
        (None,               {'fields': ['first_name']}),
        ('Date information', {'fields': ['phone'], 'classes': ['collapse']}),
    ]

    list_display = ('first_name', 'phone')
admin.site.register(Contact, ContactAdmin)
