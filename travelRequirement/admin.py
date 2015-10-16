from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from travelRequirement.models import *
# Register your models here.

class UserDetailsInline(admin.StackedInline):
    model = UserDetails
    can_delete = False
    verbose_name_plural = 'UserDetails'

# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (UserDetailsInline, )

# Re-register UserAdmin



admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(travelReq)
admin.site.register(travelPackage)
admin.site.register(daysSch)
admin.site.register(hotelDetails)
admin.site.register(airportDetails)
admin.site.register(flightDetails)
admin.site.register(feedback)
admin.site.register(feedback_files)
admin.site.register(agent_files)
admin.site.register(agent_details)
admin.site.register(UserDetails)