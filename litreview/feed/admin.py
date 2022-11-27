from django.contrib import admin

# Register your models here.
from feed.models import Ticket, Review

class TicketAdmin(admin.ModelAdmin):  # nous insérons ces deux lignes..
    list_display = ('title', 'description', 'time_created') # liste les champs que nous voulons sur l'affichage de la liste

class ReviewAdmin(admin.ModelAdmin):  # nous insérons ces deux lignes..
    list_display = ('headline', 'body', 'ticket', 'time_created') # liste les champs que nous voulons sur l'affichage de la liste


admin.site.register(Ticket, TicketAdmin)
admin.site.register(Review, ReviewAdmin)
