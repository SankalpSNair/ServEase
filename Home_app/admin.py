from django.contrib import admin
from .models import Users,Skill,House_Maid,Home_Nurse,Carpenter,Electrician,Plumber,Booking

# Register your models here.
admin.site.register(Users)
admin.site.register(Skill)
admin.site.register(House_Maid)
admin.site.register(Home_Nurse)
admin.site.register(Carpenter)
admin.site.register(Electrician)
admin.site.register(Plumber)
admin.site.register(Booking)