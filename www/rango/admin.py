from django.contrib import admin
from rango.models import Category, Page, UserProfile
from django.contrib.auth.models import User

# Register your models here.

class PageAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "url", "views")

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("website", 'picture')

admin.site.register(Page, PageAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(UserProfile, UserProfileAdmin)