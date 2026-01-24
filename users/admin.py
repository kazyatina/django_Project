from django.contrib import admin
from .models import CustomUser
# from django.contrib.auth.admin import UserAdmin

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "phone_number", "country")
    list_filter = ("country",)
    search_fields = ("email", "country", "phone_number")



# admin.site.register(UserAdmin)

