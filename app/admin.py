from django.contrib import admin
from .models import Courses, Topics, Order, Comment

admin.site.register(Courses)
admin.site.register(Topics)
admin.site.register(Order)
admin.site.register(Comment)
