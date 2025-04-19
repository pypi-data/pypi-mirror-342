from django.contrib import admin
from .models import *

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')  # Укажите поля, которые хотите отображать в списке
    search_fields = ('name',)  # Поля для поиска

class RequestAdmin(admin.ModelAdmin):
    list_display = ('service', 'user', 'status')  # Укажите поля, которые хотите отображать в списке
    list_filter = ('status',)  # Фильтры по статусу

# Регистрация моделей с настройками
admin.site.register(Service, ServiceAdmin)
admin.site.register(Request, RequestAdmin)