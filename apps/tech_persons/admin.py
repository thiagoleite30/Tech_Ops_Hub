from django.contrib import admin

from apps.tech_persons.models import *

class ListingEmployee(admin.ModelAdmin):
    list_display = ('id', 'nome', 'matricula')
    list_display_links = ('id', 'nome')
    search_fields = ('id', 'nome', 'matricula')
    list_per_page = 10

class ListingUserEmployee(admin.ModelAdmin):
    list_display = ('id', 'user', 'employee', 'emp_id')
    list_display_links = ('id',)
    search_fields = ('id', 'user')
    list_per_page = 10
    
admin.site.register(Employee, ListingEmployee)    
admin.site.register(UserEmployee, ListingUserEmployee)
