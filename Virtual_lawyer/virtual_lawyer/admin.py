from django.contrib import admin
from .models import Lawyer

# Register your models here.
class LawyerAdmin(admin.ModelAdmin):
    pass
admin.site.register(Lawyer,LawyerAdmin)