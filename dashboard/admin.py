from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = "Profile (Gemini API key)"
    readonly_fields = ("gemini_api_key", "avatar_url")
    fk_name = "user"
    max_num = 1
    extra = 0

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ("username", "email", "first_name", "last_name", "last_login", "is_staff", "date_joined")
    list_filter = ("is_staff", "is_superuser", "is_active")
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("-date_joined",)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "has_gemini_key", "avatar_url")
    list_filter = ()
    search_fields = ("user__username", "user__email")
    readonly_fields = ("user", "gemini_api_key", "avatar_url")

    def has_gemini_key(self, obj):
        return bool(obj and obj.gemini_api_key)

    has_gemini_key.boolean = True

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
