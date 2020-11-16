from django.contrib import admin
from .models import Todos

class Todoadmin(admin.ModelAdmin):
    readonly_fields=('created',)


admin.site.register(Todos, Todoadmin)
