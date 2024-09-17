from django.contrib import admin
from treeMenu.models import Menu, MenuItem


class MenuItemInline(admin.StackedInline):
    model = MenuItem
    extra = 1


class MenuAdmin(admin.ModelAdmin):
    inlines = [MenuItemInline]


admin.site.register(Menu, MenuAdmin)