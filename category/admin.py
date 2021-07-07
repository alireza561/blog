from django.contrib import admin

# Register your models here.
from .models import Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('position', 'title', 'slug', 'parent', 'status')
    list_filter = (['status'])  # Boolanfield bayad hatman besurate list dar list_filter vared shavad
    search_fields = ('title', 'slug')


admin.site.register(Category, CategoryAdmin)
