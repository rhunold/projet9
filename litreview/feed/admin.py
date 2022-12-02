from django.contrib import admin
from feed.models import Ticket, Review


class TicketAdmin(admin.ModelAdmin):
    """ Display datas of Ticket in the admin list """
    list_display = ('title', 'description', 'time_created')


class ReviewAdmin(admin.ModelAdmin):
    """ Display datas of Review in the admin list """
    list_display = ('headline', 'body', 'ticket', 'time_created')


admin.site.register(Ticket, TicketAdmin)
admin.site.register(Review, ReviewAdmin)
