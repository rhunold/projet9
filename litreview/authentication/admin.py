from django.contrib import admin

from authentication.models import User, UserFollow

class UserAdmin(admin.ModelAdmin): 
    pass
    # list_display = ('name',) # liste les champs que nous voulons sur l'affichage de la liste
    
class UserFollowAdmin(admin.ModelAdmin): 
    pass    


admin.site.register(User, UserAdmin)
admin.site.register(UserFollow, UserFollowAdmin)
