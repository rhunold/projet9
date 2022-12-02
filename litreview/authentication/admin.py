from django.contrib import admin
from authentication.models import User, UserFollow


class UserAdmin(admin.ModelAdmin):
    pass


class UserFollowAdmin(admin.ModelAdmin):
    pass

admin.site.register(User, UserAdmin)
admin.site.register(UserFollow, UserFollowAdmin)
