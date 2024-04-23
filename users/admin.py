from django.contrib import admin
from .models import Offense
# Register your models here.


@admin.register(Offense)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('title', 'content')