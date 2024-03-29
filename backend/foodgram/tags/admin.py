from django.contrib import admin

from tags.models import Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'color',
        'slug'
    )
    list_editable = ('color',)
    search_fields = ('name', 'color', 'slug')
